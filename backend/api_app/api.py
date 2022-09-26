import api_app.models as models

class User:
    def __init__(self, name, commitments, meeting_subscriptions):
        self.name, self.commitments, self.meeting_subscriptions = name, commitments, meeting_subscriptions
    
    def json_object(self):
        return {"name": self.name, "commitments": self.commitments, "meetingSubscriptions": self.meeting_subscriptions}

class Commitment:
    def __init__(self, start, end, is_absolute):
        self.start, self.end, self.is_absolute = start, end, is_absolute
    
    def json_object(self):
        return {"start": self.start, "end": self.end, "isAbsolute": self.is_absolute}

class Meeting:
    def __init__(self, name, start, end, proposals, subscribed_users, lock_in_date):
        self.name, self.start, self.end, self.proposals, self.subscribed_users, self.lock_in_date = name, start, end, proposals, subscribed_users, lock_in_date
    
    def json_object(self):
        return {"name": self.name, "start": self.start, "end": self.end, "proposals": self.proposals, "subscribedUsers": self.subscribed_users, "lockInDate": self.lock_in_date}

class MeetingTimeProposal:
    def __init__(self, start, end, commited_users, unavailable_users, optimality):
        self.start, self.end, self.commited_users, self.unavailable_users, self.optimality = start, end, commited_users, unavailable_users, optimality
    
    def json_object(self):
        return {"start": self.start, "end": self.end, "commitedUsers": self.commited_users, "unavailableUsers": self.unavailable_users, "optimality": self.optimality}

class MeetingAttendee:
    def __init__(self, user, is_critical, weight):
        self.user, self.is_critical, self.weight = user, is_critical, weight

    def json_object(self):
        return {"user": self.user, "isCritical": self.is_critical, "weight": self.weight}

class UserAttendance:
    def __init__(self, meeting, is_critical, weight):
        self.meeting, self.is_critical, self.weight = meeting, is_critical, weight
    
    def json_object(self):
        return {"meeting": self.meeting, "isCritical": self.is_critical, "weight": self.weight}

def create_user(obj):
    model = models.User.create(name=obj.name)
    for commitment in obj.commitments:
        commitment_model = models.Commitment.objects.filter(id=commitment).first()
        commitment_model.user = model.id
        commitment_model.save()
    for subscription in obj.meeting_subscriptions:
        subscription_model = models.UserMeetingSubscription.objects.filter(id=subscription).first()
        subscription_model.user = model.id
        subscription_model.save()
    return model.id

def get_user(id):
    user = models.User.objects.filter(id=id).first()
    commitment_ids = list(map(lambda com: com.id, models.Commitment.objects.filter(user=id).all()))
    meeting_subscription_ids = list(map(lambda sub: sub.id, models.Commitment.objects.filter(user=id).all()))
    return User(user.name, commitment_ids, meeting_subscription_ids)

def update_user(id, obj):
    user = models.User.objects.filter(id=id).first()
    user.name = obj.name
    user.save()

def create_commitment(obj):
    model = models.Commitment.create(start=obj.start, end=obj.end, is_absolute=obj.is_absolute)
    return model.id

def get_commitment(id):
    commitment = models.Commitment.objects.filter(id=id).first()
    return Commitment(commitment.start, commitment.end, commitment.is_absolute)

def update_commitment(id, obj):
    commitment = models.Commitment.objects.filter(id=id).first()
    commitment.start, commitment.end, commitment.is_absolute = obj.start, obj.end, obj.is_absolute
    commitment.save()

def create_meeting(obj):
    model = models.Meeting.objects.create(name=obj.name, start=obj.start, end=obj.end, lock_in_date=obj.lock_in_date)
    for proposal in model.proposals:
        proposal_model = models.MeetingTimeProposal.objects.filter(id=proposal).first()
        proposal_model.meeting = model.id
        proposal_model.save()
    for subscription in model.subscribed_users:
        subscription_model = models.UserMeetingSubscription.objects.fitler(id=subscription).first()
        subscription_model.meeting = model.id
        subscription_model.save()
    return model.id

def get_meeting(id):
    meeting = models.Meeting.objects.filter(id=id).first()
    proposal_ids = list(map(lambda prop: prop.id, models.MeetingTimeProposal.objects.filter(id=id).all()))
    subscription_ids = list(map(lambda sub: sub.id, models.UserMeetingSubscription.objects.filter(meeting=id).all()))
    return Meeting(meeting.name, meeting.start, meeting.end, proposal_ids, subscription_ids, meeting.lock_in_date)

def update_meeting(id, obj):
    meeting = models.Meeting.objects.filter(id=id).first()
    meeting.name, meeting.start, meeting.end, meeting.lock_in_date = obj.name, obj.start, obj.end, obj.lock_in_date
    meeting.save()

def create_proposal(obj):
    # BUG: if a user is in both `commited` and `unavailable`, they are saved as `unavailable`, not `commited`
    model = models.MeetingTimeProposal.objects.create(start=obj.start, end=obj.end, optimality=obj.optimality)
    for commited in model.commited_users:
        commited_model = models.MeetingProposalAttendance.objects.filter(id=commited).first()
        commited_model.is_commited = true
        commited_model.proposal = model.id
        commited_model.save()
    for unavailable in model.commited_users:
        unavailable_model = models.MeetingProposalAttendance.objects.filter(id=commited).first()
        commited_model.is_commited = false
        unavailable_model.proposal = model.id
        unavailable_model.save()
    return model.id

def get_proposal(id):
    proposal = models.Meeting.objects.filter(id=id).first()
    committed_subscription_ids = list(map(lambda att: att.user_subscription, models.MeetingProposalAttendance.objects.filter(proposal=id, is_committed=True).all()))
    unavailable_subscription_ids = list(map(lambda att: att.user_subscription, models.MeetingProposalAttendance.objects.filter(proposal=id, is_committed=False).all()))
    return MeetingTimeProposal(proposal.start, proposal.end, committed_subscription_ids, unavailable_subscription_ids, proposal.optimality)

def update_proposal(id, obj):
    proposal = models.Meeting.objects.filter(id=id).first()
    proposal.start, proposal.end, proposal.optimality = obj.start, obj.end, obj.optimality
    proposal.save()

def create_attendee(obj):
    model = models.UserMeetingSubscription.objects.create(user=obj.user, is_critical=obj.is_critical, weight=obj.weight)
    return model.id

def get_attendee(id):
    subscription = models.UserMeetingSubscription.objects.filter(id=id).first()
    return MeetingAttendee(subscription.user, subscription.is_critical, subscription.weight)

def update_attendee(id, obj):
    subscription = models.UserMeetingSubscription.objects.filter(id=id).first()
    subscription.user, subscription.is_critical, subscription.weight = obj.user, obj.is_critical, obj.weight
    subscription.save()

def create_attendance(obj):
    model = models.UserMeetingSubscription.objects.create(meeting=obj.meeting, is_critical=obj.is_critical, weight=obj.weight)
    return model.id

def get_attendance(id):
    subscription = models.UserMeetingSubscription.objects.filter(id=id).first()
    return UserAttendance(subscription.meeting, subscription.is_critical, subscription.weight)

def update_attendance(id, obj):
    subscription = models.UserMeetingSubscription.objects.filter(id=id).first()
    subscription.meeting, subscription.is_critical, subscription.weight = obj.meeting, obj.is_critical, obj.weight
    subscription.save()
