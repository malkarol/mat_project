from datetime import datetime
from django.test import TestCase
from session_handler.models import Session, Participant
import datetime
class SessionTestCase(TestCase):
    def setUp(self) -> None:
        Session.objects.create(name="HelloSession", 
        min_num_of_participants=2, max_num_of_participants=10,
        actual_num_of_participants=0, start_date=datetime.datetime(2021,12,22),
        founder_id=2
        )
    
    def test_session_hello(self):
        session = Session.objects.get(name="HelloSession")
        self.assertEqual(session.name, "HelloSession")

