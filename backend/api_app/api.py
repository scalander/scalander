import api_app.models as models
from backend.api_app.models import UserMeetingSubscription

class User:
    def __init__(self, name, commitments, meetingSubscriptions):
        self.name, self.commitments, self.meetingSubscriptions = name, commitments, meetingSubscriptions

class Commitment:
    def __init__(self, start, end, isAbsolute):
        self.start, self.end, self.isAbsolute = start, end, isAbsolute

class Meeting:
    def __init__(self, name, start, end, subscribedUsers, lockInDate):
        self.name, self.start, self.end, self.subscribedUsers, self.lockInDate = name, start, end, subscribedUsers, lockInDate

class MeetingAttendee:
    def __init__(self, user, isCritical, weight):
        self.user, self.isCritical, self.weight = user, isCritical, weight
class UserAttendence:
    def __init__(self, meeting, isCritical, weight):
        self.meeting, self.isCritical, self.weight = meeting, isCritical, weight

def get_meeting_data(id):
    mtg = models.Meeting.objects.filter(id=id).first()
    subscriptions = models.UserMeetingSubscription.objects.filter(meeting_id=mtg.id).all()
    users = list(map(lambda x: models.User.objects.filter(id=x.user_id).first(), subscriptions))
    return users

def get_user_availability(id):
    user = models.User.objects.filter(id=id).first()
    commitments = models.Commitment.objects.filter(user_id=user.id).all()
    subscriptions = models.UserMeetingSubscription.objects.filter(user_id=user.id).all()
    subs_and_meetings = list(map(lambda sub: {"subscription": sub, "meeting": UserMeetingSubscription.objects.filter(id=sub.meeting_id).first()}, subscriptions))
