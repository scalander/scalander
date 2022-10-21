import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from datetime import *
import datetime
import api_app.api as api
import environ


#TODO internationalize

ENDPOINT=("no_reply@em6498.scalander.com", "Team Scalander")
# Take environment variables from .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env() #acessing .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) #reading env file


#TODO put this somewhere
with open("./emailing/availability.html", "r") as avail:
    availability_email_text = avail.read().strip()


# def meeting_confirm
def inviteEmail(id): #takes meeting id string
    meeting = api.get_meeting(id)
    op = 0
    meetingnum = 0
    for i in range(len(meeting.proposals)): #passing through meeting time proposals to get most optimal proposal
        if meeting.proposals[i].optimality > op: #we might not need to do this passing through
            op = meeting.proposals[i].optimality
            meetingnum = i
    meetingtime = datetime.strptime(meeting.proposals[meetingnum])

    message = Mail( #describing the email to send
        from_email=ENDPOINT,
        to_emails=[api.get_user(u).emails for u in meeting.subscribed_users], # email(s) being plural is a misnomer, email is singular
        subject=f'{meeting.name} Time Confirmation',
        html_content=f'<p><h1>{meeting.name} has been scheduled for <strong>{meetingtime.start}</strong> and will last for <strong>{meeting.length}</strong>.<br><br><a href="https://scalander.com/{id}">Click Here to See Meeting Details</a></h1></p>')
    try:
        sg = SendGridAPIClient(env("SENDGRID_KEY")) #getting key from env and using it to initialize a sendgrid
        response = sg.send(message) #sending message
    except Exception as e:
        print(e.message) #if it didn't, throwing an error

def availabilityEmail(id, uid): #takes meeting id string, user id string
    meeting = api.get_meeting(id)
    user = api.get_user(uid)
    message = Mail( #describing the email to send
        from_email=ENDPOINT,
        to_emails=[user.emails], # email(s) being plural is a misnomer, email is singular
        subject=f'{meeting.name} Availability Confirmation',
        html_content=availability_email_text % {
            "meeting_name": meeting.name,
            "meeting_url": f"https://scalander.com/meeting/{id}",
            "scheduling_url": f"https://scalander.com/schedule/{uid}",
            "recipient": user.emails # its actually singular
        }) # old style format
    try:
        sg = SendGridAPIClient(env("SENDGRID_KEY")) #getting key from env and using it to initialize a sendgrid
        response = sg.send(message) #sending message
    except Exception as e:
        print(e.message) #if it didn't, throwing an error
