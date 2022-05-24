from django.contrib.auth import get_user
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


class LoginTaseCase(TestCase):
    # DRY - Don't repeat yourself
    def setUp(self):
        self.db_user = User.objects.create(username="testname", first_name="testname")
        self.db_user.set_password("test123")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "testname",
                "password": "test123"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-testname",
                "password": "test123"
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        # false
        self.client.post(
            reverse("users:login"),
            data={
                "username": "testname",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="testname", password="test123")
        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = User.objects.create(
            username="Jakhongir",
            first_name="Jakhongir",
            last_name="Rakhmonov",
            email="test@gmail.com"
        )
        user.set_password("qwqw1212")
        user.save()

        self.client.login(username="Jakhongir", password="qwqw1212")

        response = self.client.get(reverse("users:profile"))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = User.objects.create(
            username="Aziz",
            first_name="Aziz",
            last_name="John",
            email="test@gmail.com"
        )
        user.set_password("qwqw1212")
        user.save()

        self.client.login(username="Aziz", password="qwqw1212")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "Aziz",
                "first_name": "Aziz",
                "last_name": "Doe",
                "email": "done@gmail.com"
            }
        )

        user = User.objects.get(pk=user.pk)

        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "done@gmail.com")

        self.assertEqual(response.url, reverse("users:profile"))
