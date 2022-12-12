from django.test import TestCase
import datetime
import api_app.api as api
import api_app.models as models
from django.utils import timezone

ONE_HOUR = datetime.timedelta(hours=1)
ONE_DAY = datetime.timedelta(days=1)
ONE_WEEK = datetime.timedelta(days=7)

NOW = timezone.now()
IN_TWO_DAYS = NOW + (ONE_DAY*2)
IN_ONE_WEEK = NOW + ONE_WEEK

# Create your tests here.
class CreateReadTestCase(TestCase):
    # create meeting
    def test_meeting(self):
        meeting = api.Meeting("Some Meeting", NOW, IN_ONE_WEEK,
                              IN_TWO_DAYS, 30, [], [])
        meeting_id = api.create_meeting(meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        self.assertEqual(fetched_meeting.name, "Some Meeting")
        self.assertEqual(fetched_meeting.start, NOW)
        self.assertEqual(fetched_meeting.end, IN_ONE_WEEK)
        self.assertEqual(fetched_meeting.lock_in_date, IN_TWO_DAYS)
        self.assertEqual(len(fetched_meeting.proposals), 0)
        self.assertEqual(len(fetched_meeting.subscriptions), 0)
        self.assertEqual(fetched_meeting.length, 30)

        meeting.name = "A different meeting"
        api.update_meeting(meeting_id, meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        self.assertEqual(fetched_meeting.name, "A different meeting")

        api.delete_meeting(meeting_id)
        self.assertRaises(models.Commitment.DoesNotExist, lambda: api.get_commitment(meeting_id))

    # create commitment
    def test_commitment(self):
        u = api.User("John Doe", "johndoe@email.com", [])
        uid = api.create_user(u)
        commitment = api.Commitment(NOW, NOW+ONE_HOUR, True)
        
        commitment_id = api.create_commitment(commitment)
        fetched_commitment = api.get_commitment(commitment_id)
        self.assertEqual(fetched_commitment.start, NOW)
        self.assertEqual(fetched_commitment.end, NOW+ONE_HOUR)
        self.assertEqual(fetched_commitment.is_absolute, True)

        commitment_id = api.create_many_commitments(uid, [commitment])[0]
        fetched_commitment = api.get_commitments_by_user(uid)[0]
        self.assertEqual(fetched_commitment.start, NOW)
        self.assertEqual(fetched_commitment.end, NOW+ONE_HOUR)
        self.assertEqual(fetched_commitment.is_absolute, True)

        commitment.end = NOW+ONE_HOUR+ONE_HOUR
        api.update_commitment(commitment_id, commitment)
        fetched_commitment = api.get_commitments_by_user(uid)[0]
        self.assertEqual(commitment.end, NOW+ONE_HOUR+ONE_HOUR)
        
        api.delete_commitment(commitment_id)
        self.assertRaises(models.Commitment.DoesNotExist, lambda: api.get_commitment(commitment_id))

    def test_user(self):
        meeting = api.Meeting("Some Meeting", NOW, IN_ONE_WEEK,
                              IN_TWO_DAYS, 30, [], [])
        meeting_id = api.create_meeting(meeting)

        u = api.User("John Doe", "johndoe@email.com", [])
        uid = api.create_user(u)

        sub_ids = [api.create_attendance(api.UserAttendance(uid, meeting_id, True, 0))]

        api.update_user(uid, 
                        api.User("John Doe", "johndoe@email.com", sub_ids))

        fetched_user = api.get_user(uid)
        self.assertEqual(fetched_user.name, "John Doe")
        self.assertEqual(fetched_user.email, "johndoe@email.com")
        self.assertSequenceEqual(fetched_user.subscriptions, sub_ids)

        api.delete_user(uid)
        self.assertRaises(models.User.DoesNotExist, lambda: api.get_user(uid))
        
    def test_meeting_proposal_create(self):
        proposal = api.MeetingTimeProposal(None, NOW, NOW+ONE_HOUR, [], [], 10000)
        proposal_id = api.create_proposal(proposal)
        meeting = api.Meeting("Some Meeting", NOW, NOW+ONE_DAY, NOW+ONE_WEEK, 30, [proposal_id], [])
        meeting_id = api.create_meeting(meeting)
        fetched_meeting = api.get_meeting(meeting_id)
        fetched_proposal = api.get_proposal(fetched_meeting.proposals[0])
        self.assertEqual(fetched_proposal.start, NOW)
        self.assertEqual(fetched_proposal.end, NOW+ONE_HOUR)
        self.assertEqual(len(fetched_proposal.committed_attendences), 0)
        self.assertEqual(len(fetched_proposal.unavailable_attendences), 0)
        self.assertEqual(fetched_proposal.optimality, 10000)

        api.delete_proposal(proposal_id)
        self.assertRaises(models.MeetingTimeProposal.DoesNotExist, lambda: api.get_proposal(proposal_id))

    def test_meeting_attendance_create(self):
        user = api.User("Teddy", "the@the.com", [])
        user_id = api.create_user(user)
        meeting = api.Meeting("A meeting!", NOW, NOW+ONE_DAY, NOW+ONE_WEEK, 30, [], [])
        meeting_id = api.create_meeting(meeting)
        attendance = api.UserAttendance(user_id, meeting_id, True, 190)
        att_id = api.create_attendance(attendance)
        fetched_meeting = api.get_meeting(meeting_id)
        fetched_attendance = api.get_attendance(fetched_meeting.subscriptions[0])
        self.assertEqual(fetched_attendance.user, user_id)
        self.assertEqual(fetched_attendance.meeting, meeting_id)
        self.assertEqual(fetched_attendance.is_critical, True)
        self.assertEqual(fetched_attendance.weight, 190)

        uid = api.get_uid_by_subscription(att_id)
        self.assertEqual(user_id, uid)

        fetched_user = api.get_user_by_subscription(att_id)
        self.assertEqual(fetched_user.name, "Teddy")
        
        attendance.weight = 1900
        api.update_attendance(att_id, attendance)

        fetched_attendance = api.get_attendance(att_id)
        self.assertEqual(fetched_attendance.weight, 1900)

        api.delete_attendance(att_id)
        self.assertRaises(models.UserMeetingSubscription.DoesNotExist, lambda: api.get_attendance(att_id))
