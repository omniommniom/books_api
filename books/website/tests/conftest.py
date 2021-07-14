import os
import sys

import pytest
# from rest_framework.test import APIClient

from .utils import create_fake_books, create_authors, create_categories

sys.path.append(os.path.dirname(__file__))

# sys.path.append(os.path.dirname(__file__))
# #
# # sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"website"))

@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def set_up():
    create_categories()
    create_authors()
    # for _ in range(8):
    #     Category.objects.create(name=faker.name())
    # for _ in range(12):
    #     Author.objects.create()
    for _ in range(10):
        create_fake_books()


