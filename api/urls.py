from django.urls import path
from .views import BookReviewAPIView, BookListAPIView

app_name = "api"

urlpatterns = [
    path("reviews/", BookListAPIView.as_view(), name="review-list"),
    path("reviews/<int:id>/", BookReviewAPIView.as_view(), name="review-detail"),
]
