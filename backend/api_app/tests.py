from django.test import TestCase
import datetime
import api_app.api as api

# Create your tests here.
class UserTestCase(TestCase):
    def test_user_create(self):
        c = api.Commitment(datetime.datetime.now(), datetime.datetime.now(), False)
        commitment_ids = [api.create_commitment(c), api.create_commitment(c), api.create_commitment(c)]
        m = api.Meeting("Some Meeting", datetime.datetime.now(), datetime.datetime.now(), 30, [], [], datetime.datetime.now())
        m_id = api.create_meeting(m)
        sub = api.UserAttendance(m_id, True, 0)
        sub_ids = [api.create_attendance(sub)]
        u = api.User("John Doe", "johndoe@email.com", commitment_ids, sub_ids)
        uid = api.create_user(u)
        fetched_user = api.get_user(uid)
        r_sub_ids = fetched_user.meeting_subscriptions
        r_sub_ids.sort()
        sub_ids.sort()
        r_com_ids = fetched_user.commitments
        r_com_ids.sort()
        commitment_ids.sort()
        self.assertEqual(fetched_user.name, "John Doe")
        self.assertEqual(fetched_user.emails, "johndoe@email.com")
        self.assertEqual(r_com_ids, commitment_ids)
        self.assertEqual(r_sub_ids, sub_ids)
    
    def test_meeting_create(self):
        now = datetime.datetime.now()
        meeting = api.Meeting("Some Meeting", now, now, now, 30, [], [])
        meeting_id = api.create_meeting(meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        self.assertEqual(fetched_meeting.name, "Some Meeting")
        self.assertEqual(fetched_meeting.start, now)
        self.assertEqual(fetched_meeting.end, now)
        self.assertEqual(fetched_meeting.lock_in_date, now)
        self.assertEqual(len(fetched_meeting.proposals), 0)
        self.assertEqual(len(fetched_meeting.subscriptions), 0)
        self.assertEqual(fetched_meeting.length, 30)

    def test_meeting_proposal_create(self):
        now = datetime.datetime.now()
        proposal = api.MeetingTimeProposal(None, now, now, [], [], 10000)
        proposal_id = api.create_proposal(proposal)
        meeting = api.Meeting("Some Meeting", now, now, now, 30, [proposal_id], [])
        meeting_id = api.create_meeting(meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        fetched_proposal = api.get_proposal(fetched_meeting.proposals[0])
        self.assertEqual(fetched_proposal.start, now)
        self.assertEqual(fetched_proposal.end, now)
        self.assertEqual(len(fetched_proposal.committed_attendences), 0)
        self.assertEqual(len(fetched_proposal.unavailable_attendences), 0)
        self.assertEqual(fetched_proposal.optimality, 10000)

    def test_meeting_attendance_create(self):
        user = api.User("Teddy", "the@the.com", [])
        user_id = api.create_user(user)
        attendance = api.UserAttendance(user_id, None, True, 190)
        att_id = api.create_attendance(attendance)
        now = datetime.datetime.now()
        meeting = api.Meeting("A meeting!", now, now, now, 30, [], [att_id])
        meeting_id = api.create_meeting(meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        fetched_attendance = api.get_attendance(meeting.subscriptions[0])
        self.assertEqual(fetched_attendance.user, user_id)
        self.assertEqual(fetched_attendance.meeting, meeting_id)
        self.assertEqual(fetched_attendance.is_critical, True)
        self.assertEqual(fetched_attendance.weight, 190)
        fetched_user = api.get_user(user_id)
        fetched_attendance = api.get_attendance(user.subscriptions[0])
        self.assertEqual(fetched_attendance.user, user_id)
        self.assertEqual(fetched_attendance.meeting, meeting_id)
        self.assertEqual(fetched_attendance.is_critical, True)
        self.assertEqual(fetched_attendance.weight, 190)

    def test_commitment_create(self):
        user = api.User("Teddy", "the@the.com", [])
        user_id = api.create_user(user)
        now = datetime.datetime.now()
        commitment = api.Commitment(now, now, False)
        commitment_id = api.create_commitment(commitment)
        fetched_commitment = api.get_commitment(commitment_id)
        self.assertEqual(fetched_commitment.start, now)
        self.assertEqual(fetched_commitment.end, now)
        self.assertEqual(fetched_commitment.is_absolute, False)
