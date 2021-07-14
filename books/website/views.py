import requests
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from website.forms import ChooseQuery
from website.models import Book, Category, Author
from website.ordering import MyCustomOrdering
from website.serializers import BookSerializer, QuerySerializer


class ChooseQueryView(APIView):
    def get(self, request):
        form = ChooseQuery()
        return render(request, 'main.html', {'form': form})


    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            URL = "https://www.googleapis.com/books/v1/volumes"
            PARAMS = {'q': query}
            res = requests.get(url=URL, params=PARAMS)
            data = res.json()
            if res.status_code == 200:
                books = data['items']
                for book in books:
                    try:
                        average_rating = book['volumeInfo']['averageRating']
                    except KeyError:
                        average_rating = 0
                    try:
                        ratings_count = book['volumeInfo']['ratingsCount']
                    except KeyError:
                        ratings_count = 0
                    try:
                        categories = book['volumeInfo']['categories']
                    except KeyError:
                        categories = []
                    try:
                        thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
                    except KeyError:
                        thumbnail = ""
                    title = book['volumeInfo']['title']
                    authors = book['volumeInfo']['authors']
                    published_date = int(book['volumeInfo']['publishedDate'][:4])

                    if Book.objects.filter(title=title,
                                           published_date=published_date
                                           ).exists():
                        aut = Author.objects.filter(book_authors__in=Book.objects.filter(title=title, published_date=published_date))
                        # book_db = Book.objects.get(title=title, published_date=published_date, authors__in=aut)
                        book_db = Book.objects.get(title=title, published_date=published_date, authors=aut[0])
                        book_db.thumbnail = thumbnail
                        book_db.average_rating = average_rating
                        book_db.ratings_count = ratings_count
                        book_db.save()

                    else:
                        book_db = Book.objects.create(
                            title=title,
                            published_date=published_date,
                            thumbnail=thumbnail,
                            average_rating=average_rating,
                            ratings_count=ratings_count
                        )

                    if categories:
                        for category in categories:
                            cat, created = Category.objects.get_or_create(name=category)
                            book_db.categories.add(cat)

                    if authors:
                        for author in authors:
                            # breakpoint()
                            first_name, last_name = author.split(" ", 1)
                            aut, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
                            book_db.authors.add(aut)


                for book in books:
                    serializer = BookSerializer(Book.objects.all(), many=True)
                    # serializer.data
                    # content = JSONRenderer().render(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # class SnippetSerializer(serializers.Serializer):
                    #     id = serializers.IntegerField(read_only=True)
                    #     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
                    #     code = serializers.CharField(style={'base_template': 'textarea.html'})
                    #     linenos = serializers.BooleanField(required=False)
                    #     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
                    #     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
                    #
                    #     def create(self, validated_data):
                    #         """
                    #         Create and return a new `Snippet` instance, given the validated data.
                    #         """
                    #         return Snippet.objects.create(**validated_data)
                    #
                    #     def update(self, instance, validated_data):
                    #         """
                    #         Update and return an existing `Snippet` instance, given the validated data.
                    #         """
                    #         instance.title = validated_data.get('title', instance.title)
                    #         instance.code = validated_data.get('code', instance.code)
                    #         instance.linenos = validated_data.get('linenos', instance.linenos)
                    #         instance.language = validated_data.get('language', instance.language)
                    #         instance.style = validated_data.get('style', instance.style)
                    #         instance.save()
                    #         return instance


                    # BookSerializer(instance = )



# class ChooseQueryView(APIView):
#     def get(self, request):
#         form = ChooseQuery()
#         return render(request, 'main.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = ChooseQuery(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             URL = "https://www.googleapis.com/books/v1/volumes"
#             PARAMS = {'q': query}
#             res = requests.get(url=URL, params=PARAMS)
#             data = res.json()
#             if res.status_code == 200:
#                 books = data['items']
#                 for book in books:
#                     try:
#                         average_rating = book['volumeInfo']['averageRating']
#                     except KeyError:
#                         average_rating = 0
#                     try:
#                         ratings_count = book['volumeInfo']['ratingsCount']
#                     except KeyError:
#                         ratings_count = 0
#                     try:
#                         categories = book['volumeInfo']['categories']
#                     except KeyError:
#                         categories = []
#                     try:
#                         thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
#                     except KeyError:
#                         thumbnail = ""
#                     title = book['volumeInfo']['title']
#                     authors = book['volumeInfo']['authors']
#                     published_date = int(book['volumeInfo']['publishedDate'][:4])
#
#                     if Book.objects.filter(title=title,
#                                            published_date=published_date
#                                            ).exists():
#                         aut = Author.objects.filter(book_authors__in=Book.objects.filter(title=title, published_date=published_date))
#                         # book_db = Book.objects.get(title=title, published_date=published_date, authors__in=aut)
#                         book_db = Book.objects.get(title=title, published_date=published_date, authors=aut[0])
#                         book_db.thumbnail = thumbnail
#                         book_db.average_rating = average_rating
#                         book_db.ratings_count = ratings_count
#                         book_db.save()
#
#                     else:
#                         book_db = Book.objects.create(
#                             title=title,
#                             published_date=published_date,
#                             thumbnail=thumbnail,
#                             average_rating=average_rating,
#                             ratings_count=ratings_count
#                         )
#
#                     if categories:
#                         for category in categories:
#                             cat, created = Category.objects.get_or_create(name=category)
#                             book_db.categories.add(cat)
#
#                     if authors:
#                         for author in authors:
#                             first_name, last_name = author.split(" ", 1)
#                             aut, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
#                             book_db.authors.add(aut)
#
#             ctx = {'books': books}
#             return render(request, 'books.html', ctx)
#         ctx = {'form': form}
#         return render(request, 'main.html', ctx)

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [MyCustomOrdering, ]
    ordering_fields = ['published_date']


    def get_queryset(self):
        queryset = Book.objects.all()
        published_date = self.request.query_params.get('published_date')
        authors = self.request.query_params.getlist('author')
        if len(authors) != 0:
            breakpoint()
            if len(authors) == 1:
                a1fn, a1ln = authors[0].split(" ", 1)
                aut1 = Author.objects.filter(first_name=a1fn, last_name=a1ln)
                queryset = queryset.filter(authors=aut1[0])
            else:
                a1fn, a1ln = authors[0].split(" ", 1)
                a2fn, a2ln = authors[1].split(" ", 1)
                aut1 = Author.objects.filter(first_name=a1fn, last_name=a1ln)
                aut2 = Author.objects.filter(first_name=a2fn, last_name=a2ln)
                queryset = queryset.filter(authors=aut1[0]).filter(authors=aut2[0])

        if published_date is not None:
            queryset = queryset.filter(published_date=published_date)

        return queryset


class BookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
