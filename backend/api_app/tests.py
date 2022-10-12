from django.test import TestCase
import datetime
import api_app.api as api

# Create your tests here.
class UserTestCase(TestCase):
    def test_user_create(self):
        c = api.Commitment(datetime.datetime.now(), datetime.datetime.now(), False)
        commitment_ids = [api.create_commitment(c), api.create_commitment(c), api.create_commitment(c)]
        m = api.Meeting("Some Meeting", datetime.datetime.now(), datetime.datetime.now(), [], [], datetime.datetime.now())
        m_id = api.create_meeting(m)
        sub = api.UserAttendance(m_id, True, 0)
        sub_ids = [api.create_attendance(sub)]
        u = api.User("John Doe", "johndoe@email.com", commitment_ids, sub_ids)
        uid = api.create_user(u)
        fetched_user = api.get_user(uid)
        self.assertTrue(fetched_user.name == "John Doe")
        self.assertTrue(fetched_user.email == "johndoe@email.com")
        self.assertTrue(fetched_user.commitments == commitment_ids)
        self.assertTrue(fetched_user.meeting_subscriptions == sub_ids)