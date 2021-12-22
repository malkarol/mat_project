from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.test import TestCase
from account.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create( email = "usertest@gmail.com",
        username = "usertest", first_name= "karol", last_name="kowalski",
        password = "somePASS")

    def test_user_model_create(self):
        user = User.objects.get(username = "usertest")
        # Then
        self.assertEqual(user.username, "usertest")

    def test_user_mode_email(self):
        user = User.objects.get(username = "usertest")
        try:
            validate_email(user.email)
        except ValidationError:
            self.fail("Wrong email format")

# class UserEndpointsTestCase(TestCase):
#     def setUp(self)


    