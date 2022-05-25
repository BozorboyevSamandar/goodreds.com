from django.views.generic import ListView, DetailView

from books.models import Book


# Create your views here.

class BookView(ListView):
    template_name = "books/list.html"
    queryset = Book.objects.all()
    context_object_name = "books"


# class BookView(View):
#     def get(self, request):
#         books = Book.objects.all()
#         return render(request, "books/list.html", {"books": books})

class BookDetailView(DetailView):
    template_name = "books/detail.html"
    pk_url_kwarg = "id"
    model = Book

# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#
#         return render(request, "books/detail.html", {"book": book})
