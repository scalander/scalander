import datetime
#import api_app.api as api
import os
import sendgrid
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import environ

ics = '''BEGIN:VCALENDAR
PRODID:-//Scalander//Scalander//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
DTSTART:{DTStart}
DTEND:{DTEnd}
DTSTAMP:{DTStamp}
ORGANIZER;CN=Scalander:mailto:scalandersupp@gmail.com
UID:{Meeting_Id}@url.com
{Attendees}
CREATED:{DTStamp}
DESCRIPTION:Placeholder
LAST-MODIFIED:{DTStamp}
LOCATION:Placeholder
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:{Title}
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR'''
attendeeTemplate = "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={name};X-NUM-GUESTS=0:{email}"
testvalues = {"Title":"test", 'DTStart':'20221023T200000Z',"DTEnd":"20221023T210000Z","DTStamp":"20221023T190000Z","Meeting_Id":"blahblahblah","Attendees":attendeeTemplate}
x=datetime.datetime.now()
def datetime_to_ics(time):
    time2=[str(time.month),str(time.day),str(time.hour),str(time.minute),str(time.second)]
    for i in range(len(time2)):
        if len(time2[i]) == 1:
            time2[i] = "0"+time2[i]
    newtime=str(time.year)+time2[0]+time2[1]+"T"+time2[2]+time2[3]+time2[4]+"Z"
    return newtime
def generate_ics(id): #takes in id of meeting
    values = {"Title": "", 'DTStart': '', "DTEnd": "", "DTStamp": "", "Meeting_Id": "", "Attendees":""}
    meeting = api.get_meeting(id)
    for i in range(len(meeting.proposals)):  # passing through meeting time proposals to get most optimal proposal
        if meeting.proposals[i].optimality > op:  # we might not need to do this passing through
            op = meeting.proposals[i].optimality
            meetingnum = i
    meetingtime = meeting.proposals[meetingnum]
    values["Title"]=meeting.name
    values["DTStart"] = datetime_to_ics(meetingtime.start)
    values["DTEnd"] = datetime_to_ics(meetingtime.end)
    values["DTStamp"] = datetime_to_ics(datetime.datetime.now())
    attendees=""
    for i in range(len(meetingtime.commitedUsers)):
        name=meetingtime.commitedUsers[i].user.name
        email=meetingtime.commitedUsers[i].user.email
        attendees+=attendeeTemplate.format(name=name,email=email)
        if i != len(meetingtime.commitedUsers) - 1:
            attendees += "\n"
    values["Attendees"] = attendees
    new_ics = ics.format(**values)
    print(new_ics)
    return new_ics


ENDPOINT=("no_reply@em6498.scalander.com", "Team Scalander")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env() #acessing .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def meetingEmail(ics,id): #ics file to send and meeting id
    meeting = api.get_meeting(id)
    message = Mail(  # describing the email to send
        from_email=ENDPOINT,
        to_emails=[api.get_user(u).email for u in meeting.subscribed_users],
        subject=f'{meeting.name} Time Confirmation',
        html_content=f'<p><h1>{meeting.name} has been scheduled, please add it to your calendar. Thank you!</h1></p>')

    encoded_ics = ics.encode("utf-8")
    encoded_file = base64.b64encode(encoded_ics).decode()
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('invite.ics'),
        FileType('application/ics'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    sg = SendGridAPIClient(env("SENDGRID_KEY"))  # getting key from env and using it to initialize a sendgrid
    response = sg.send(message)  # sending message