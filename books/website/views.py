from django.shortcuts import render
from django.views import View
from rest_framework import generics, filters

import requests

from website.forms import ChooseQuery
from website.models import Book
from website.serializers import BookSerializer
from website.ordering import MyCustomOrdering


class ChooseQueryView(View):
    def get(self, request):
        form = ChooseQuery()
        return render(request, 'main.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChooseQuery(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            URL = "https://www.googleapis.com/books/v1/volumes"
            PARAMS = {'q': query}
            res = requests.get(url=URL, params=PARAMS)
            data = res.json()
            if res.status_code == 200:
                books = data['items']
                for book in books:
                    try:
                        title = book['volumeInfo']['title']
                        authors = book['volumeInfo']['authors']
                        published_date = int(book['volumeInfo']['publishedDate'][:4])
                        categories = book['volumeInfo']['categories']
                        average_rating = book['volumeInfo']['averageRating']
                        ratings_count = book['volumeInfo']['ratingsCount']
                        thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
                        # check if books is already in database:
                        if Book.objects.filter(title=title).exists():
                            book_db = Book.objects.get(title=title)
                            book_db.authors = authors
                            book_db.published_date = published_date
                            book_db.categories = categories
                            book_db.thumbnail = thumbnail
                            book_db.average_rating = average_rating
                            book_db.ratings_count = ratings_count
                            book_db.save()
                        else:
                            book_new = Book.objects.create(title=title, authors=authors,
                                                           published_date=published_date,
                                                           categories=categories,
                                                           average_rating=average_rating,
                                                           ratings_count=ratings_count,
                                                           thumbnail=thumbnail
                                                           )
                    except KeyError:
                        pass
                    # if 'categories' in book['volumeInfo']:
                    #     categories = book['volumeInfo']['categories']
                    # else:
                    #     categories = []
                    # if 'averageRating' in book['volumeInfo']:
                    #     average_rating = book['volumeInfo']['averageRating']
                    # else:
                    #     average_rating = 0
                    # if 'ratingsCount' in book['volumeInfo']:
                    #     ratings_count = book['volumeInfo']['ratingsCount']
                    # else:
                    #     ratings_count = 0
                    # if 'thumbnail' in book['volumeInfo']['imageLinks']:
                    #     thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
                    # else:
                    #     thumbnail = ""


            ctx = {'books': books}
            return render(request, 'books.html', ctx)
        ctx = {'form': form}
        return render(request, 'main.html', ctx)

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    # queryset = Book.objects.all()
    filter_backends = [MyCustomOrdering, ]
    ordering_fields = ['published_date']


    def get_queryset(self):
        queryset = Book.objects.all()
        published_date = self.request.query_params.get('published_date')
        author = self.request.query_params.get('author')
        authors = " ".join(self.request.query_params.getlist('author'))

        # breakpoint()
        if published_date is not None:
            queryset = queryset.filter(published_date=published_date)
        # if author is not None:
        #     queryset = queryset.filter(authors__icontains=author)

        if authors is not None:
            queryset = queryset.filter(authors__icontains=authors)
            # queryset.filter(Q(authors__icontains=author_name) | Q(authors__icontains=author_name))
        return queryset


class BookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
