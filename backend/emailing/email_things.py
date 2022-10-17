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


### IMPORTS

import sendgrid
import os
from datetime import *
import datetime


### VARIABLES

meeting = Meeting()  # I presume Theodore will add the actual meeting input


# to = [
#     {"email": "john@doe.com", "name": "John Doe"}, 
#     {"email": "sara@calendlysux.xyz", "name": "Sara Doe"}
# ]


sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))  # still need api key
data = {
  "personalizations": [
    {
      "to": [{"email": u.user.email, "name": u.user.name} for u in meeting.subscribedUsers],
      "subject": f"{meeting.name} Confirmed From {meeting.start.isoformat(timespec="minutes")} To {meeting.end.isoformat(timespec="minutes")}"
    }
  ],
  "from": {
    "email": "test@example.com"  # whatever the email linked to sendgrid is, not sure of this yet
  },
  "content": [
    {
      "type": "text/plain",  # for now just plaintext, will format more later
      "value": f"The Meeting \"{meeting.name}\" has been scheduled to start at {meeting.start.isoformat(timespec="minutes")} and end at {meeting.end.isoformat(timespec="minutes")}, lasting a total of {(meeting.end - meeting.start).total_seconds() // 60} minutes."  # format a bit better later, including the datetime iso format
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)