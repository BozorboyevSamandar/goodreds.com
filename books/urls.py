from django.urls import path
from books.views import BookView, BookDetailView

app_name = 'books'


urlpatterns = [
    path("", BookView.as_view(), name="list"),
    path("<int:id>/", BookDetailView.as_view(), name="detail")
]