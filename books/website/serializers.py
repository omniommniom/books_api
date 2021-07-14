from rest_framework import serializers
from website.models import Book, Category, Author


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'published_date', 'average_rating', 'ratings_count', 'categories', 'thumbnail']


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()