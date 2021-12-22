from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.test import TestCase
from account.models import User

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

class UserTestCase(TestCase):
    def setUp(self):
        # When
        User.objects.create( email = "usertest@gmail.com",
        username = "usertest", first_name= "karol", last_name="kowalski",
        password = "somePASS")

    def test_user_model_create(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.assertEqual(user.username, "usertest")

    def test_user_mode_email(self):
        user = User.objects.get(username = "usertest")
        # Then
        try:
            validate_email(user.email)
        except ValidationError:
            self.fail("Wrong email format")

    def test_username_length(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.failIf(len(user.username) > 20)

    def test_firstname_length(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.failIf(len(user.first_name) > 20)

    def test_lasstname_length(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.failIf(len(user.last_name) > 20)

    def test_user_firstname_containsdigits(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.failIf(has_numbers(user.first_name))

    def test_user_lastname_containsdigits(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.failIf(has_numbers(user.last_name))

# class UserEndpointsTestCase(TestCase):
#     def setUp(self)


    