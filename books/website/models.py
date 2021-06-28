from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    # authors = models.ManyToManyField(Author, related_name="book_authors")
    authors = models.CharField(max_length=255)
    # categories = models.ManyToManyField(Category, related_name="book_categories")
    categories = models.CharField(max_length=255)
    published_date = models.IntegerField()
    average_rating = models.IntegerField(default=0)
    ratings_count = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=255)

