from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.test import TestCase
from rest_framework.parsers import JSONParser
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

class UserListViewTest(TestCase):
    @classmethod
    def setUp(cls):
        number_of_users = 10
        for user_id in range(number_of_users):
            User.objects.create( email = f"user{user_id}test@gmail.com",
        username = f"user{user_id}test", first_name= f"karol{user_id}", last_name="kowalski",
        password = f"somePASS{user_id}")

    def test_userview_url_exists_at_desired_location(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_lists_all_users(self):
        response = self.client.get('/users/')
        #user_data = JSONParser().parse(response.items)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)



    