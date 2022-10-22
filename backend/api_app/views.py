import json
from django.views import View
from django.http import JsonResponse, HttpResponse
import api_app.api as api
from google_api.get_freebusy import get_freebusy

class User(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(name=data["name"], email=data["email"])
        model_id = api.create_user(obj)
        return JsonResponse({"status": "success", "id": model_id})

    def get(self, request, id):
        obj = api.get_user(id)
        return JsonResponse(obj.__dict__)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.User(name=data["name"], email=data["email"])
        api.update_user(id, obj)
        api.schedule_user(obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_user(id)
        return HttpResponse(status=204)

class Commitment(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Commitment(start=data["start"], end=data["end"], is_absolute=data["isAbsolute"])
        model_id = api.create_commitment(obj)
        return HttpResponse(status=201, headers={"Location": model_id})

    def get(self, request, id):
        obj = api.get_commitment(id)
        return JsonResponse(obj.__dict__)
    
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
        obj = api.Meeting(name=data["name"], start=data["start"],
                          end=data["end"], length=data["length"],
                          lock_in_date=data["lockInDate"])
        model_id = api.create_meeting(obj)
        return JsonResponse({"status": "success", "id": model_id})

    def get(self, request, id):
        obj = api.get_meeting(id)
        return JsonResponse(obj.__dict__)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.Meeting(name=data["name"], start=data["start"],
                          end=data["end"], length=data["length"], lock_in_date=data["lockInDate"])
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
        return JsonResponse({"status": "success", "id": model_id})

    def get(self, request, id):
        obj = api.get_proposal(id)
        # we need to serialize this custom-ly because
        # it has foreign keys in it
        return JsonResponse({
            "start": obj.start,
            "end": obj.end,
            "commitedUsers": list(map(lambda x:api.get_user_by_subscription(x.id).__dict__, obj.committed_attendences)),
            "unavailableUsers": list(map(lambda x:api.get_user_by_subscription(x.id).__dict__, obj.unavailable_attendences))
        });
   
    def delete(self, request, id):
        api.delete_proposal(id)
        return HttpResponse(status=204)

class Attendance(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(meeting=data["meeting"], user=data["user"],
                                 is_critical=data["isCritical"], weight=data["weight"])
        model_id = api.create_attendance(obj)
        return JsonResponse({"status": "success", "id": model_id})

    def get(self, request, id):
        obj = api.get_attendance(id)
        return JsonResponse(obj.__dict__)
    
    def put(self, request, id):
        data = json.loads(request.body.decode("utf-8"))
        obj = api.UserAttendance(meeting=data["meeting"], is_critical=data["isCritical"], weight=data["weight"])
        api.update_attendance(id, obj)
        return HttpResponse(status=204)

    def delete(self, request, id):
        api.delete_attendance(id)
        return HttpResponse(status=204)

class FreeBusy(View):
    def get(self, request):
        auth_header = auth_code=request.headers["Authorization"]
        if len(auth_header.split(" ")) < 2:
            return HttpResponse(status=401)
        obj = get_freebusy(auth_code=auth_header.split(" ")[1])
        return JsonResponse(obj)

class ManyCommitments(View):
    def post(self, request, id):
        commitment_list = json.loads(request.body.decode("utf-8"))
        api.create_many_commitments(id, [api.Commitment(start=i["start"],
                                                        end=i["end"],
                                                        is_absolute=i["isAbsolute"]) for i in commitment_list])
        obj = api.get_user(id)
        api.schedule_user(obj)
        return HttpResponse(status=204)
