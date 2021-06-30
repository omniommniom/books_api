from rest_framework import serializers
from models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['title', 'authors', 'categories', 'published_date', 'average_rating', 'categories', 'authors', 'thumbnail']