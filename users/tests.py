from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class RegistrationTaseCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "Jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Rakhimov",
                "email": "test@gmail.com",
                "password": "qwqw1212"
            }
        )

        user = User.objects.get(username="Jakhongir")

        self.assertEqual(user.first_name, "Jakhongir")
        self.assertEqual(user.last_name, "Rakhimov")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertNotEqual(user.password, "qwqw1212")
        self.assertTrue(user.check_password("qwqw1212"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Jakhongir",
                "email": "test@gmail.com",
            }
        )
        user_count = User.objects.count()

        self.assertEqual(user_count, 0)

        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Rakhimov",
                "email": "invalid-email",
                "password": "qwqw1212"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1. create a user
        user = User.objects.create(
            username="Jakhongir",
            first_name="Jakhonkir"
        )
        user.set_password("1212qwqw")
        user.save()
        
        # 2. TRy to create another user with that same username
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Rakhimov",
                "email": "invalid-email",
                "password": "qwqw1212"
            }
        )
        # 3. check that the second user was not created
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response, "form", "username", "A user with that username already exists.")
