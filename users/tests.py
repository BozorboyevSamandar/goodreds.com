from django.contrib.auth.models import User
from django.test import TestCase


# Create your tests here.

class RegistrationTaseCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            "/users/register",
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
        self.assertEqual(user.last_name, "Jakhongir")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertNotEqual(user.password, "qwqw1212")
        self.assertTrue(user.check_password("qwqw1212"))