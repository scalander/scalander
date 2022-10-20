import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from datetime import *
import datetime
import api_app.api as api
import datetime

#TODO internationalize

ENDPOINT=no_reply@em6498.scalander.com

# def meeting_confirm

meeting = api.Meeting()

meeting_datetime = datetime.strptime(meeting.

message = Mail(
    from_email=ENDPOINT,
    to_emails=[api.get_user(u).emails for u in meeting.subscribed_users], # email(s) being plural is a misnomer, email is singular
    subject=f'{meeting.name} Time Confirmation',
    html_content=f'<p><h1>{meeting.name} has been scheduled for <strong>{a}</strong> and will last for <strong>{format_length((meeting.end-meeting.start).total_seconds()//60)}</strong>.<br><br><a href="http://scalander.com/{meetingID}">Click Here to See Meeting Details</a></h1></p>')
try:
    sg = SendGridAPIClient(os.environ.get(apikey))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
