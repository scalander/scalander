import api_app.models as models

class User:
    def __init__(self, name, emails, commitments, meeting_subscriptions):
        self.name, self.emails, self.commitments, self.meeting_subscriptions = name, emails, commitments, meeting_subscriptions
    
    def json_object(self):
        return {"name": self.name, "emails": self.emails, "commitments": self.commitments, "meetingSubscriptions": self.meeting_subscriptions}

class Commitment:
    def __init__(self, start, end, is_absolute):
        self.start, self.end, self.is_absolute = start, end, is_absolute
    
    def json_object(self):
        return {"start": self.start, "end": self.end, "isAbsolute": self.is_absolute}

class Meeting:
    def __init__(self, name, start, end, length, proposals, subscribed_users, lock_in_date):
        self.name, self.start, self.end, self.length, self.proposals, self.subscribed_users, self.lock_in_date = name, start, end, length, proposals, subscribed_users, lock_in_date
    
    def json_object(self):
        return {"name": self.name, "start": self.start, "end": self.end, "length": self.length, "proposals": self.proposals, "subscribedUsers": self.subscribed_users, "lockInDate": self.lock_in_date}

class MeetingTimeProposal:
    def __init__(self, start, end, committed_users, unavailable_users, optimality):
        self.start, self.end, self.committed_users, self.unavailable_users, self.optimality = start, end, committed_users, unavailable_users, optimality
    
    def json_object(self):
        return {"start": self.start, "end": self.end, "committedUsers": self.committed_users, "unavailableUsers": self.unavailable_users, "optimality": self.optimality}

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
    model = models.User.objects.create(name=obj.name, email=obj.emails)
    for commitment in obj.commitments:
        commitment_model = models.Commitment.objects.get(id=commitment)
        commitment_model.user_id = model.id
        commitment_model.save()
    for subscription in obj.meeting_subscriptions:
        subscription_model = models.UserMeetingSubscription.objects.get(id=subscription)
        subscription_model.user_id = model.id
        subscription_model.save()
    return model.id

def get_user(id):
    user = models.User.objects.get(id=id)
    commitment_ids = list(map(lambda com: com.id, models.Commitment.objects.filter(user_id=id).all()))
    meeting_subscription_ids = list(map(lambda sub: sub.id, models.UserMeetingSubscription.objects.filter(user_id=id).all()))
    return User(user.name, user.email, commitment_ids, meeting_subscription_ids)

def update_user(id, obj):
    user = models.User.objects.get(id=id)
    user.name = obj.name
    user.emails = obj.emails
    user.save()

    # Update commitments
    commitment_models = dict(map(lambda com: (com.id, com), models.Commitment.objects.filter(user_id=id).all()))
    current_commitments = set(commitment_models.keys())
    to_attach = set(obj.commitments) - current_commitments
    to_delete = current_commitments - set(obj.commitments)
    for commitment_id in to_attach:
        commitment = models.Commitment.objects.filter(id=commitment_id).first()
        commitment.user_id = id
        commitment.save()
    for commitment_id in to_delete:
        commitment = commitment_models[commitment_id]
        commitment.delete()
    
    # Update meeting subscriptions
    subscription_models = dict(map(lambda com: (com.id, com), models.UserMeetingSubscription.objects.filter(user_id=id).all()))
    current_subscriptions = set(subscription_models.keys())
    to_attach = set(obj.meeting_subscriptions) - current_subscriptions
    to_delete = current_subscriptions - set(obj.meeting_subscriptions)
    for subscription_id in to_attach:
        subscription = subscription_models[subscription_id]
        subscription.user_id = id
        subscription.save()
    for subscription_id in to_delete:
        # TODO: [OPTIMIZE] extra db query here, and everywhere else this strategy is used
        delete_subscription(id)

def delete_user(id):
    user_model = models.User.objects.filter(id=id)
    commitment_models = models.Commitment.objects.filter(user=id).all()
    for commitment in commitment_models:
        commitment.delete()
    subscription_models = models.UserMeetingSubscription.objects.filter(user=id).all()
    for subscription in subscription_models:
        proposal_attendance_models = models.MeetingProposalAttendance.objects.filter(user_subscription_id=subscription.id).all()
        for proposal_attendance in proposal_attendance_models:
            proposal_attendance.delete()
        subscription.delete()
    user_model.delete()

def create_commitment(obj):
    model = models.Commitment.objects.create(start=obj.start, end=obj.end, is_absolute=obj.is_absolute)
    return model.id

def get_commitment(id):
    commitment = models.Commitment.objects.get(id=id)
    return Commitment(commitment.start, commitment.end, commitment.is_absolute)

def update_commitment(id, obj):
    commitment = models.Commitment.objects.get(id=id)
    commitment.start, commitment.end, commitment.is_absolute = obj.start, obj.end, obj.is_absolute
    commitment.save()

def delete_commitment(id):
    commitment = models.Commitment.objects.get(id=id)
    commitment.delete()

def create_meeting(obj):
    model = models.Meeting.objects.create(name=obj.name, start=obj.start, end=obj.end, length=obj.length, lock_in_date=obj.lock_in_date)
    for proposal in obj.proposals:
        proposal_model = models.MeetingTimeProposal.objects.get(id=proposal)
        proposal_model.meeting_id = model.id
        proposal_model.save()
    for subscription in obj.subscribed_users:
        subscription_model = models.UserMeetingSubscription.objects.get(id=subscription)
        subscription_model.meeting_id = model.id
        subscription_model.save()
    return model.id

def get_meeting(id):
    meeting = models.Meeting.objects.get(id=id)
    subscription_ids = list(map(lambda sub: sub.id, models.UserMeetingSubscription.objects.filter(meeting_id=id).all()))

    # sort proposal by optimality (higher better, so reverse order)
    proposals = models.MeetingTimeProposal.objects.filter(meeting=meeting).order_by("-optimality")
    proposal_ids = list(map(lambda prop: prop.id, proposals))
    
    return Meeting(meeting.name, meeting.start, meeting.end, meeting.length, proposal_ids, subscription_ids, meeting.lock_in_date)

def update_meeting(id, obj):
    meeting = models.Meeting.objects.get(id=id)
    meeting.name, meeting.start, meeting.end, meeting.length, meeting.lock_in_date = obj.name, obj.start, obj.end, obj.length, obj.lock_in_date
    meeting.save()

    # Update time proposals
    proposal_models = dict(map(lambda com: (com.id, com), models.MeetingTimeProposal.objects.filter(meeting=id).all()))
    current_proposals = set(map(lambda com: com.id, proposal_models))
    to_attach = set(obj.proposals) - current_proposals
    to_delete = current_proposals - set(obj.proposals)
    for proposal_id in to_attach:
        proposal = models.MeetingTimeProposal.objects.filter(id=proposal_id).first()
        proposal.meeting = meeting
        proposal.save()
    for proposal_id in to_delete:
        delete_proposal(proposal_id)

    # Update user subscription
    subscription_models = dict(map(lambda com: (com.id, com), models.UserMeetingSubscription.objects.filter(meeting=id).all()))
    current_subscriptions = set(subscription_models.keys())
    to_attach = set(obj.subscribed_users) - current_subscriptions
    to_delete = current_subscriptions - set(obj.subscribed_users)
    for subscription_id in to_attach:
        subscription = models.UserMeetingSubscription.objects.get(id=subscription_id)
        subscription.meeting = id
        subscription.save()
    for subscription_id in to_delete:
        delete_subscription(subscription_id)

def delete_meeting(id):
    meeting = models.Meeting.objects.get(id=id)
    proposal_models = models.MeetingTimeProposal.objects.filter(meeting=id).all()
    for proposal in proposal_models:
        attendance_models = models.MeetingProposalAttendance.objects.filter(proposal_id=proposal.id).all()
        for attendance in attendance_models:
            attendance.delete()
        proposal.delete()
    subscription_models = models.UserMeetingSubscription.objects.filter(user=id).all()
    for subscription in subscription_models:
        subscription.delete()
    meeting.delete()

def create_proposal(obj):
    # BUG: if a user is in both `committed` and `unavailable`, they are saved as `unavailable`, not `committed`
    model = models.MeetingTimeProposal.objects.create(start=obj.start, end=obj.end, optimality=obj.optimality)
    for committed in obj.committed_users:
        committed_model = models.MeetingProposalAttendance.objects.create(proposal_id=model.id, user_subscription_id=committed, is_committed=True)
    for unavailable in obj.committed_users:
        unavailable_model = models.MeetingProposalAttendance.objects.create(proposal_id=model.id, user_subscription_id=committed, is_committed=False)
    return model.id

def get_proposal(id):
    proposal = models.MeetingTimeProposal.objects.get(id=id)
    committed_subscription_ids = list(map(lambda att: att.user_subscription, models.MeetingProposalAttendance.objects.filter(proposal_id=id, is_committed=True).all()))
    unavailable_subscription_ids = list(map(lambda att: att.user_subscription, models.MeetingProposalAttendance.objects.filter(proposal_id=id, is_committed=False).all()))
    return MeetingTimeProposal(proposal.start, proposal.end, committed_subscription_ids, unavailable_subscription_ids, proposal.optimality)

def update_proposal(id, obj):
    proposal = models.MeetingTimeProposal.objects.get(id=id)
    proposal.start, proposal.end, proposal.optimality = obj.start, obj.end, obj.optimality
    proposal.save()

    # Update committed users
    committed_user_models = dict(map(lambda com: (com.id, com), models.MeetingProposalAttendance.objects.filter(proposal=id, is_committed=True).all()))
    current_committed_users = set(map(lambda com: com.id, committed_user_models))
    to_attach = set(obj.committed_users) - current_committed_users
    to_delete = current_committed_users - set(obj.committed_users)
    for committed_user_id in to_attach:
        committed_user = committed_user_models[committed_user_id]
        committed_user.user_id = id
        committed_user.save()
    for committed_user_id in to_delete:
        committed_user = committed_user_models[committed_user_id]
        committed_user.delete()
    
    # Updated unavailable users
    unavailable_user_models = dict(map(lambda com: (com.id, com), models.MeetingProposalAttendance.objects.filter(proposal=id, is_committed=False).all()))
    current_unavailable_users = set(map(lambda com: com.id, unavailable_user_models))
    to_attach = set(obj.unavailable_users) - current_unavailable_users
    to_delete = current_unavailable_users - set(obj.unavailable_users)
    for unavailable_user_id in to_attach:
        unavailable_user = unavailable_user_models[unavailable_user_id]
        unavailable_user.user_id = id
        unavailable_user.save()
    for unavailable_user_id in to_delete:
        unavailable_user = unavailable_user_models[unavailable_user_id]
        unavailable_user.delete()

def delete_proposal(id):
    proposal = models.Meeting.objects.get(id=id)
    attendance_models = models.MeetingProposalAttendance.objects.filter(proposal=id).all()
    for attendance in attendance_models:
        attendance.delete()
    proposal.delete()

def create_attendee(obj):
    model = models.UserMeetingSubscription.objects.create(user_id=obj.user, is_critical=obj.is_critical, weight=obj.weight)
    return model.id

def get_attendee(id):
    subscription = models.UserMeetingSubscription.objects.get(id=id)
    return MeetingAttendee(subscription.user_id, subscription.is_critical, subscription.weight)

def update_attendee(id, obj):
    subscription = models.UserMeetingSubscription.objects.get(id=id)
    subscription.user_id, subscription.is_critical, subscription.weight = obj.user, obj.is_critical, obj.weight
    subscription.save()

def delete_attendee(id):
    delete_subscription(id)

def create_attendance(obj):
    model = models.UserMeetingSubscription.objects.create(meeting_id=obj.meeting, is_critical=obj.is_critical, weight=obj.weight)
    return model.id

def get_attendance(id):
    subscription = models.UserMeetingSubscription.objects.get(id=id)
    return UserAttendance(subscription.meeting_id, subscription.is_critical, subscription.weight)

def update_attendance(id, obj):
    subscription = models.UserMeetingSubscription.objects.get(id=id)
    subscription.meeting_id, subscription.is_critical, subscription.weight = obj.meeting, obj.is_critical, obj.weight
    subscription.save()

def delete_attendance(id):
    delete_subscription(id)

def delete_subscription(id):
    subscription = models.UserMeetingSubscription.objects.get(id=id)
    subscription.delete()

def create_many_commitments(id, commitments):
    # deletes previous commitments
    models.Commitment.objects.filter(user_id=id).delete()
    for c in commitments:
        c = models.Commitment.objects.create(start=c["start"], end=c["end"],
                                             is_absolute=True,
                                             user_id=id)
