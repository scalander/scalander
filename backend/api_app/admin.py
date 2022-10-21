from django.contrib import admin
import api_app.models as models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Meeting)
admin.site.register(models.Commitment)
admin.site.register(models.UserMeetingSubscription)
admin.site.register(models.MeetingTimeProposal)
