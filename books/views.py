from django.shortcuts import render
from django.views import View
from books.models import Book


# Create your views here.


class BookView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, "books/list.html", {"books": books})


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        return render(request, "books/detail.html", {"book": book})
