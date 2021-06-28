from django.shortcuts import render
from django.views import View
import requests

from .forms import ChooseQuery
from .models import Book


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
                            # average_ratings=averageRating,
                            # ratings_count=ratingsCount,
                        book_db.save()
                ctx = {'books': books}
                return render(request, 'books.html', ctx)
            else:
                pass
        ctx = {'form': form}
        return render(request, 'main.html', ctx)

#
# class AddStudentView(View):
#     def get(self, request, *args, **kwargs):
#         form = AddStudentForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'exercises_app/add_student.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = AddStudentForm(request.POST)
#         if form.is_valid():
#             #zapisać do bazy
#             first_name = form.cleaned_data['name']
#             last_name = form.cleaned_data['surname']
#             school_class = form.cleaned_data['class_name']
#             year_of_birth = form.cleaned_data['year_of_birth']
#
#             student = Student.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 school_class=school_class,
#                 year_of_birth=year_of_birth,
#             )
#             return redirect(f'/student/{student.pk}/')
#         else:
#             context = {'form': form}
#             return render(request, 'exercises_app/add_student.html', context)