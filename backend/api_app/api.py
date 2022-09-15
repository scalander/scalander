import api_app.models as models

class User:
    def __init__(self, name, commitments, meeting_subscriptions):
        self.name, self.commitments, self.meeting_subscriptions = name, commitments, meeting_subscriptions

class Commitment:
    def __init__(self, start, end, is_absolute):
        self.start, self.end, self.is_absolute = start, end, is_absolute

class Meeting:
    def __init__(self, name, start, end, proposals, subscribed_users, lock_in_date):
        self.name, self.start, self.end, self.proposals, self.subscribed_users, self.lock_in_date = name, start, end, proposals, subscribed_users, lock_in_date

class MeetingTimeProposal:
    def __init__(self, start, end, commited_users, unavailable_users, optimality):
        self.start, self.end, self.commited_users, self.unavailable_users, self.optimality = start, end, commited_users, unavailable_users, optimality

class MeetingAttendee:
    def __init__(self, user, is_critical, weight):
        self.user, self.is_critical, self.weight = user, is_critical, weight
class UserAttendance:
    def __init__(self, meeting, is_critical, weight):
        self.meeting, self.is_critical, self.weight = meeting, is_critical, weight

def get_user(id):
    user = models.User.objects.filter(id=id).first()
    commitment_ids = list(map(lambda com: com.id, models.Commitment.objects.filter(user=id).all()))
    meeting_subscription_ids = list(map(lambda sub: sub.id, models.Commitment.objects.filter(user=id).all()))
    return User(user.name, commitment_ids, meeting_subscription_ids)