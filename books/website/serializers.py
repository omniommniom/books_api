from rest_framework import serializers
from website.models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['title', 'authors', 'categories', 'published_date', 'average_rating', 'ratings_count', 'categories', 'authors', 'thumbnail']