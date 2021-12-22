from datetime import datetime
from django.db import models
from django.test import TestCase
from session_handler.models import Session, Participant, SessionResult
from datetime import datetime,date
from ml_handler.models import MLModel
from account.models import User

class SetUpHelper():
    '''
    Helper class for creating and saving objects necessary for model test.
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

    def setUpSessionResult():
        return SessionResult.objects.create(local_models_accuracy_json="accuracy: 80%", finished=True)


class AssertHelper():
    '''
    Helper class for creating and saving objects necessary for model test.
    '''
    def dummyUser():
        return User( email = "usertest@gmail.com",
        username = "usertest", first_name= "usertest", last_name="usertest",
        password = "somePASS")

    def dummyModel(user):
        return MLModel(name = "test model",
        creation_date = "2021-12-11",
        model_parameters_json = "one param",
        owner = user)

    def dummyParticipant():
        user= AssertHelper.dummyUser()
        model= AssertHelper.dummyModel(user)
        return Participant(user = user, model = model)

    def dummySession():
        return Session(name="Test Session",
        min_num_of_participants=2, max_num_of_participants=10,
        actual_num_of_participants=0, start_date=datetime(2021,12,22),
        founder = SetUpHelper.setUpParticipant()
        )

class ParticipantTestCase(TestCase):
    def setUp(self):
        # Given
        user= SetUpHelper.setUpUser()
        model= SetUpHelper.setUpModel(user)
        # When
        Participant.objects.create(user = user, model = model)

    def test_participant_model_create(self):
        participant = Participant.objects.get(user__username = "usertest")
        # Then
        self.assertEqual(participant.user.username, "usertest")

    def test_participant_user_notnull(self):
        participant = Participant.objects.get(user__username = "usertest")
        self.failIf(participant.user is None)

class SessionTestCase(TestCase):
    def setUp(self):
         # Given
        _name="Test Session"
        _min_num_of_participants = 2
        _max_num_of_participants = 10
        _actual_num_of_participants = 0
        _start_date = datetime(2021,12,22)
        _end_date = datetime(2021,12,30)
        _founder = SetUpHelper.setUpParticipant()
        # When
        Session.objects.create(
            name=_name,
            min_num_of_participants =_min_num_of_participants,
            max_num_of_participants =_max_num_of_participants,
            actual_num_of_participants =_actual_num_of_participants,
            start_date = _start_date,
            end_date = _end_date,
            founder = _founder
        )

    def test_session_model_create(self):
        session = Session.objects.get(founder__user__username = "usertest")
        # Then
        self.assertEqual(session.founder.user.username, "usertest" )
    
    def test_session_enddate_smaller_than_startdate(self):
        session = Session.objects.get(founder__user__username = "usertest")
        proper_date = session.start_date <= session.end_date and session.end_date >= date.today()
        self.assertEqual(proper_date, True)

    def test_session_maxparticipants_GT_minparticipants(self):
        session = Session.objects.get(founder__user__username = "usertest")
        condition = session.min_num_of_participants < session.max_num_of_participants \
            and session.min_num_of_participants >= 0 and session.actual_num_of_participants >=0
        self.assertEqual(condition, True)

class SessionResultTestCase(TestCase):
    def setUp(self):
        # Given
        _local_models_accuracy_json="accuracy: 80%"
        _finished=True
        # When
        SessionResult.objects.create(
            local_models_accuracy_json=_local_models_accuracy_json,
            finished=_finished,
            global_model = SetUpHelper.setUpModel(SetUpHelper.setUpUser())
        )

    def test_session_result_model(self):
        session_result = SessionResult.objects.get(global_model__owner__username = "usertest")
        # Then
        self.assertEqual(session_result.global_model.owner.username, "usertest" )

