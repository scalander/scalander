import json
from django.views import View
from django.http import JsonResponse, HttpResponse
import api_app.api as api

class User(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(**data)
        model_id = api.create_user(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_user(id)
        return JsonResponse(obj)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(**data)
        api.update_user(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_user(id)
        return HttpResponse(status=204)

class Commitment(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Commitment(**data)
        model_id = api.create_commitment(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_commitment(id)
        return JsonResponse(obj)
    
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
        obj = api.Meeting(**data)
        model_id = api.create_meeting(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_meeting(id)
        return JsonResponse(obj)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Meeting(**data)
        api.update_meeting(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_meeting(id)
        return HttpResponse(status=204)

class Proposal(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingTimeProposal(**data)
        model_id = api.create_proposal(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_proposal(id)
        return JsonResponse(obj)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingTimeProposal(**data)
        api.update_proposal(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_proposal(id)
        return HttpResponse(status=204)

class Attendee(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingAttendee(**data)
        model_id = api.create_attendee(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_attendee(id)
        return JsonResponse(obj)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.MeetingAttendee(**data)
        api.update_attendee(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_attendee(id)
        return HttpResponse(status=204)

class Attendance(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(**data)
        model_id = api.create_attendance(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_attendance(id)
        return JsonResponse(obj)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(**data)
        api.update_attendance(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_attendance(id)
        return HttpResponse(status=204
