from datetime import datetime
from django.db import models
from django.test import TestCase
from session_handler.models import Session, Participant
from datetime import datetime
from ml_handler.models import MLModel
from account.models import User

class SetUpHelper():
    '''
    Helper class for filling objects necessary for model test.
    '''
    def setUpUser():
        return User.objects.create( email = "usertest@gmail.com",
        username = "usertest", first_name= "usertest", last_name="usertest",
        password = "somePASS")

    def setUpModel(user):
        return MLModel.objects.create(name = "test model",
        creation_date = "2021-12-11",
        model_parameters_json = "one param",
        owner = user)

    def setUpParticipant():
        user= SetUpHelper.setUpUser()
        model= SetUpHelper.setUpModel(user)
        return Participant.objects.create(user = user, model = model)

class ParticipantTestCase(TestCase):
    def setUp(self):
        user= SetUpHelper.setUpUser()
        model= SetUpHelper.setUpModel(user)
        Participant.objects.create(user = user, model = model)

    def test_session_hello(self):
        participant = Participant.objects.get(user_id = 1)
        self.assertEqual(participant.user.username, "usertest")

class SessionTestCase(TestCase):
    def setUp(self):
        Session.objects.create(name="Test Session",
        min_num_of_participants=2, max_num_of_participants=10,
        actual_num_of_participants=0, start_date=datetime(2021,12,22),
        founder = SetUpHelper.setUpParticipant()
        )

    def test_session_hello(self):
        session = Session.objects.get(session_id = 1)
        self.assertEqual(session.name, "Test Session")

