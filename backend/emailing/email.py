# import sendgrid
# import os
# from sendgrid.helpers.mail import *

# sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("test@example.com")
# to_email = To("test@example.com")
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, to_email, subject, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)


# sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))  # still need api key
# data = {
#   "personalizations": [
#     {
#       "to": [{"email": u.user.email, "name": u.user.name} for u in meeting.subscribedUsers],
#       "subject": f"{meeting.name} Time Confirmation"
#       # "subject": f"{meeting.name} Confirmed from {meeting.start.isoformat(timespec="minutes")} to {meeting.end.isoformat(timespec="minutes")}"
#     }
#   ],
#   "from": {
#     "email": "test@example.com"  # whatever the email linked to sendgrid is, not sure of this yet
#   },
#   "content": [
#     {
#         "type": "text/html",
#         "value": f"<html><h1>{meeting.name} has been scheduled for </h1></html>"
#     #   "type": "text/plain",  # for now just plaintext, will format more later
#     #   "value": f"The Meeting \"{meeting.name}\" has been scheduled to start at {meeting.start.isoformat(timespec="minutes")} and end at {meeting.end.isoformat(timespec="minutes")}, lasting a total of {(meeting.end - meeting.start).total_seconds() // 60} minutes."  # format a bit better later, including the datetime iso format
#     }
#   ]
# }
# response = sg.client.mail.send.post(request_body=data)
# print(response.status_code)
# print(response.body)
# print(response.headers)

### IMPORTS

import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from datetime import *
import datetime


### Test Classes

class User:
    def __init__(self, name, email, commitments, meetingSubscriptions, id):
        self.name, self.email, self.commitments, self.meetingSubscriptions, self.id = name, email, commitments, meetingSubscriptions, id  # id is apparently a 5 number string for now (I generate it in tests as 10000-99999)

class Commitment: 
    def __init__(self, start, end, isAbsolute):
        self.start, self.end, self.isAbsolute = start, end, isAbsolute

class Meeting:
    def __init__(self, name, start, end, subscribedUsers, lockInDate):
        self.name, self.start, self.end, self.subscribedUsers, self.lockInDate = name, start, end, subscribedUsers, lockInDate

class MeetingAttendee:
    def __init__(self, user, isCritical, weight):
        self.user, self.isCritical, self.weight = user, isCritical, weight

class UserAttendence:
    def __init__(self, meeting, isCritical, weight):
        self.meeting, self.isCritical, self.weight = meeting, isCritical, weight

### VARIABLES

meetingID = "scalandergobrrr"
apikey = ""
now = datetime.datetime.now()
meeting = Meeting(
    "Aardvark Advocates Annual Assembly",
    now,
    now+timedelta(minutes=312),
    [
        User(
            "Aaron Ash",
            "jachuhs@nuevaschool.org",
            [],
            [],
            "35323"
        ),
        User(
            "Amber Alan",
            "jackhuhs@gmail.com",
            [],
            [],
            "76545"
        )
    ],
    now
)  # I presume Theodore will add the actual meeting input


def format_day(day):
    day = str(day)
    if day[-1] == "1" and day != "11":
        return day+"st"
    if day[-1] == "2" and day != "12":
        return day+"nd"
    if day[-1] == "3" and day != "13":
        return day+"rd"
    return day+"th"

def fix_time_format(hour, minute):
    ampm = "AM"
    hour = str(hour)
    minute = str(minute)
    if len(hour) == 1:
        hour = "0"+hour
    if len(minute) == 1:
        minute = "0"+minute
    if int(hour) > 12:
        hour = str(int(hour)-12)
        ampm = "PM"
    return f"{hour}:{minute} {ampm}"

def format_length(mins):
    hours = mins // 60
    mins -= hours*60
    hoursf = ""
    if hours > 0:
        hoursf = str(hours)+" hour"
        if hours > 1:
            hoursf += "s"
        if mins > 0:
            hoursf += " and "
    minsf = ""
    if mins > 0:
        minsf = str(mins)+" minute"
        if mins > 1:
            minsf += "s"
    return hoursf+minsf
    

setTZ = "PST"
weekdays = ["Monday", "Teusday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
startFormatted = f"{weekdays[meeting.start.weekday()]}, {months[meeting.start.month-1]} {format_day(meeting.start.day)} at {fix_time_format(meeting.start.hour, meeting.start.minute)} {setTZ}"
print(startFormatted)

message = Mail(
    from_email='no_reply@em6498.scalander.com',
    to_emails=[u.user.email for u in meeting.subscribedUsers],
    subject=f'{meeting.name} Time Confirmation',
    html_content=f'<p><h1>{meeting.name} has been scheduled for <strong>{startFormatted}</strong> and will last for <strong>{format_length((meeting.end-meeting.start).total_seconds()//60)}</strong>.<br><br><a href="http://scalander.com/{meetingID}">Click Here to See Meeting Details</a></h1></p>')
try:
    sg = SendGridAPIClient(os.environ.get(apikey))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)