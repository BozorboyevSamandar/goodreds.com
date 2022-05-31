from django.urls import path
from books.views import BookView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, DeleteReviewView

app_name = 'books'

urlpatterns = [
    path("", BookView.as_view(), name="list"),
    path("<int:id>/", BookDetailView.as_view(), name="detail"),
    path("<int:id>/reviews/", AddReviewView.as_view(), name="reviews"),
    path("<int:book_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name="edit_review"),
    path("<int:book_id>/reviews/<int:review_id>/delete/conform/", ConfirmDeleteReviewView.as_view(), name="conform_delete_review"),
    path("<int:book_id>/reviews/<int:review_id>/delete/", DeleteReviewView.as_view(), name="delete_review"),
]
