import json
from django.views import View
from django.http import JsonResponse, HttpResponse
import api_app.api as api
from scheduling.scheduling import schedule, Block
from google_api.get_freebusy import get_freebusy

class User(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(name=data["name"], emails=data["emails"], commitments=data["commitments"], meeting_subscriptions=data["meetingSubscriptions"])
        model_id = api.create_user(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_user(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(name=data["name"], emails=data["emails"], commitments=data["commitments"], meeting_subscriptions=data["meetingSubscriptions"])
        api.update_user(id, obj)
        self.schedule_meeting(obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_user(id)
        return HttpResponse(status=204)
    
    def schedule_meeting(self, user):
        for m_id in user.meeting_subscriptions:
            sub = api.get_attendance(m_id)
            meeting = api.get_meeting(sub.meeting)
            results = schedule([Block(meeting.start, meeting.end)], meeting.length, meeting.lock_in_date, meeting.subscribed_users, 5, 5, meeting.name)
            # TODO: more accurate optimality calculation
            new_proposals = list(map(lambda result: api.MeetingTimeProposal(result["start"], result["end"], result["can"], result["cannot"], sum(list(map(lambda s: api.get_attendee(s).weight, result["can"])))), results))
            meeting.proposals = list(map(lambda p: api.create_proposal(p), new_proposals))
            api.update_meeting(meeting, sub.meeting)

class Commitment(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Commitment(start=data["start"], end=data["end"], is_absolute=data["isAbsolute"])
        model_id = api.create_commitment(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_commitment(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Commitment(**data)
        api.update_commitment(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_commitment(id)
        return HttpResponse(status=204)

class Meeting(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Meeting(name=data["name"], start=data["start"], end=data["end"], proposals=data["proposals"], subscribed_users=data["subscribedUsers"], lock_in_date=data["lockInDate"])
        model_id = api.create_meeting(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_meeting(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Meeting(name=data["name"], start=data["start"], end=data["end"], proposals=data["proposals"], subscribed_users=data["subscribedUsers"], lock_in_date=data["lockInDate"])
        api.update_meeting(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_meeting(id)
        return HttpResponse(status=204)

class Proposal(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingTimeProposal(start=data["start"], end=data["end"], committed_users=data["committedUsers"], unavailable_users=data["unavailableUsers"], optimality=data["optimality"])
        model_id = api.create_proposal(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_proposal(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingTimeProposal(start=data["start"], end=data["end"], committed_users=data["committedUsers"], unavailable_users=data["unavailableUsers"], optimality=data["optimality"])
        api.update_proposal(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_proposal(id)
        return HttpResponse(status=204)

class Attendee(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingAttendee(user=data["user"], is_critical=data["isCritical"], weight=data["weight"])
        model_id = api.create_attendee(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_attendee(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingAttendee(user=data["user"], is_critical=data["isCritical"], weight=data["weight"])
        api.update_attendee(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_attendee(id)
        return HttpResponse(status=204)

class Attendance(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(meeting=data["meeting"], is_critical=data["isCritical"], weight=data["weight"])
        model_id = api.create_attendance(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_attendance(id)
        return JsonResponse(obj.json_object())
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(meeting=data["meeting"], is_critical=data["isCritical"], weight=data["weight"])
        api.update_attendance(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_attendance(id)
        return HttpResponse(status=204)

class FreeBusy(View):
    def get(self, request, id):
        auth_header = auth_code=request.headers["Authorization"]
        if len(auth_header.split(" ")) < 2:
            return HttpResponse(status=401)
        obj = get_freebusy(auth_code=auth_header.split(" ")[1])
        return JsonResponse(obj)