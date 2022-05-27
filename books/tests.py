from django.test import TestCase
from django.urls import reverse
from books.models import Book


# Create your tests here.


class BookTaseCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found")

    def test_books_title(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="13232112")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="13232112")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="13232112")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
            self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="13232112")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_book(self):
        book1 = Book.objects.create(title="sport", description="Description1", isbn="13232112")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="13232112")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="13232112")

        response = self.client.get(reverse("books:list")+"?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)
