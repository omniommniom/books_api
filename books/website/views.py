from django.shortcuts import render
from django.views import View
from rest_framework import generics

import requests

from website.forms import ChooseQuery
from website.models import Book
from website.serializers import BookSerializer


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
                    title = book['volumeInfo']['title']

                    authors = book['volumeInfo']['authors']
                    publishedDate = int((book['volumeInfo']['publishedDate'][:3]))
                    categories = book['volumeInfo']['categories']
                    try:
                        averageRating = book['volumeInfo']['averageRating']
                    except:
                        averageRating = 0
                    try:
                        ratingsCount = book['volumeInfo']['ratingsCount']
                    except:
                        ratingsCount = 0
                    thumbnail = book['volumeInfo']['imageLinks']['thumbnail']

                    # check if books is already in database:
                    if Book.objects.get(title=title,authors=authors,published_date=publishedDate):
                        book_db = Book.objects.get(title=title,authors=authors,published_date=publishedDate)
                        book_db.categories=categories
                        book_db.categories=categories
                        book_db.thumbnail=thumbnail
                        book_db.average_ratings=averageRating,
                        book_db.ratings_count=ratingsCount,
                        book_db.save()
                ctx = {'books': books}
                return render(request, 'books.html', ctx)
            else:
                pass
        ctx = {'form': form}
        return render(request, 'main.html', ctx)

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        published_date = self.request.query_params.get('published_date')

        author = self.request.query_params.get('author')
        if published_date is not None:
            queryset = queryset.filter(published_date=published_date)
        if author is not None:
            queryset = queryset.filter(authors__contains=author)
        return queryset

# class BookListView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class BookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
