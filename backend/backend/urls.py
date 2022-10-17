"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# TODO: remove CSRF exemptions
from django.views.decorators.csrf import csrf_exempt
import api_app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/<str:id>', csrf_exempt(views.User.as_view())),
    path('api/user', csrf_exempt(views.User.as_view(http_method_names=['post']))),
    path('api/commitment/<str:id>', csrf_exempt(views.Commitment.as_view())),
    path('api/commitment', csrf_exempt(views.Commitment.as_view(http_method_names=['post']))),
    path('api/meeting/<str:id>', csrf_exempt(views.Meeting.as_view())),
    path('api/meeting', csrf_exempt(views.Meeting.as_view(http_method_names=['post']))),
    path('api/proposal/<str:id>', csrf_exempt(views.Proposal.as_view())),
    path('api/proposal', csrf_exempt(views.Proposal.as_view(http_method_names=['post']))),
    path('api/attendee/<str:id>', csrf_exempt(views.Attendee.as_view())),
    path('api/attendee', csrf_exempt(views.Attendee.as_view(http_method_names=['post']))),
    path('api/attendance/<str:id>', csrf_exempt(views.Attendance.as_view())),
    path('api/attendance', csrf_exempt(views.Attendance.as_view(http_method_names=['post']))),
    path('api/freebusy/', csrf_exempt(views.FreeBusy.as_view(http_method_names=['get']))),
    path('api/many-commitments/<str:id>', csrf_exempt(views.ManyCommitments.as_view(http_method_names=['post'])))
]
