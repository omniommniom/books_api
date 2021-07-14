from random import sample, randint, choice
from faker import Faker
import names

from website.models import Author, Category, Book

faker = Faker("en_US")

# Author

def create_name():
    first_name = names.get_first_name()
    last_name = names.get_laast_name()
    return first_name, last_name

def create_authors():
    for author in range(0, 12):
        first_name, last_name = create_name()
        Author.objects.create(
            first_name=first_name,
            last_name=last_name
        )

def random_author():
    """Return a random Author object from db."""
    author = Author.objects.all()
    return choice(author)


# Category

def create_categories():
    for category in range(0, 8):
        Category.objects.create(
            name=faker.word()
        )

def random_category():
    """Return a random Category object from db."""
    category = Category.objects.all()
    return choice(category)


# Book

def fake_book_data():
    """Generate a dict of book data"""
    book_data = {
        "items": [
            {
            "volumeInfo": {
                "title": "Hobbit czyli tam i z powrotem",
                "authors": [
                "Jan Kowalski"
                # sample(list(author), randint(1,3))
                ],
                "publishedDate": int(faker.year())
                },
            "categories": [
            "History"
            # sample(list(category), randint(1, 2))
            ],
            "imageLinks": {
                "thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
            },
            "averageRating": randint(0,10),
            "ratingsCount": randint(1,10)
            }
            ]
            }
    # authors = sample(list(author), randint(1,3))
    # author_names = [(a.first_name + a.last_name) for a in authors]
    # book_data['volumeInfo']["authors"] = author_names
    #
    # categories = sample(list(category), randint(1,3))
    # category_names = [c.name for c in categories]
    # book_data['categories'] = category_names

    return book_data



def create_fake_books():
    """Generate new fake book and save to database."""
    book_data = fake_book_data()
    authors = book_data['items']['volumeInfo']["authors"]
    del book_data['items']['volumeInfo']["authors"]
    categories = book_data['items']['categories']
    new_book = Book.objects.create(**book_data)
    new_book.categories.add(random_category())
    new_book.authors.add(random_author())


# def create_fake_movie():
#     """Generate new fake movie and save to database."""
#     movie_data = fake_movie_data()
#     movie_data["director"] = find_person_by_name(movie_data["director"])
#     actors = movie_data["actors"]
#     del movie_data["actors"]
#     new_movie = Movie.objects.create(**movie_data)
#     for actor in actors:
#         new_movie.actors.add(find_person_by_name(actor))
