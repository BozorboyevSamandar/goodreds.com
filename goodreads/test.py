from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="13232112")

        user = CustomUser.objects.create(
            username="Jakhongir",
            first_name="Jakhongir",
            last_name="Rakhmonov",
            email="test@gmail.com"
        )
        user.set_password("qwqw1212")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="very good book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="nine book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="very good")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
