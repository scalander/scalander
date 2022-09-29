import json
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import api_app.models as models
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
