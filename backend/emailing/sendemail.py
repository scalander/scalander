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
AVAILABILITY_EMAIL_TEMPLATE="d-85e6eb3f7b524d36bfb557cf0796b60e"

# Emanuel mode (i.e. debug)
DONTDOIT = False


# Take environment variables from .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env() #acessing .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) #reading env file

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
        to_email=[api.get_user(u).emails for u in meeting.subscribed_users], 
        subject=f'{meeting.name} Time Confirmation',
        html_content=f'<p><h1>{meeting.name} has been scheduled for <strong>{meetingtime.start}</strong> and will last for <strong>{meeting.length}</strong>.<br><br><a href="https://scalander.com/{id}">Click Here to See Meeting Details</a></h1></p>')
    try:
        if not DONTDOIT:
            sg = SendGridAPIClient(env("SENDGRID_KEY")) #getting key from env and using it to initialize a sendgrid
            response = sg.send(message) #sending message
        else:
            print(message)
    except Exception as e:
        print(e) #if it didn't, throwing an error

def availabilityEmail(id, uid): #takes meeting id string, user id string
    meeting = api.get_meeting(id)
    user = api.get_user(uid)
    message = Mail( #describing the email to send
        from_email=ENDPOINT,
        to_emails=[user.emails], # email(s) being plural is a misnomer, email is singular
        subject=f'Finding time for {meeting.name}')

    message.template_id = AVAILABILITY_EMAIL_TEMPLATE

    message.dynamic_template_data = {
        "meeting_name": meeting.name,
        "meeting_url": f"https://scalander.com/meeting/{id}",
        "scheduling_url": f"https://scalander.com/schedule/{uid}",
        "recipient": user.emails # its actually singular
    }

    try:
        if not DONTDOIT:
            sg = SendGridAPIClient(env("SENDGRID_KEY")) #getting key from env and using it to initialize a sendgrid
            response = sg.send(message) #sending message
        else:
            print(message)
    except Exception as e:
        print(e) #if it didn't, throwing an error
