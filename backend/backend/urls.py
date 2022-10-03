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
import api_app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/<str:id>/', views.User.as_view()),
    path('api/commitment/<str:id>/', views.Commitment.as_view()),
    path('api/meeting/<str:id>/', views.Meeting.as_view()),
    path('api/proposal/<str:id>/', views.Proposal.as_view()),
    path('api/attendee/<str:id>/', views.Attendance.as_view()),
    path('api/attendance/<str:id>/', views.Attendance.as_view()),
]
