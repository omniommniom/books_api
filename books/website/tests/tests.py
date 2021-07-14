import pytest

from website.models import Book, Author, Category
from .utils import fake_movie_data, random_person



@pytest.mark.django_db
def test_get_book_list(client, set_up):
    response = client.get("/books/", {}, format='json')

    assert response.status_code == 200
    assert Book.objects.count() == len(response.data)
#

# @pytest.mark.django_db
# def test_get_movie_detail(client, set_up):
#     book = Book.objects.first()
#     response = client.get(f"/books/{book.id}/", {}, format='json')
#
#     assert response.status_code == 200
#     for field in ("title", "published_date", "average_rating", "ratings_count"):
#         assert field in response.data
#
