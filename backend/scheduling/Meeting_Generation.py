
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = build('calendar', 'v3', credentials=creds)

event_template = {
  'summary': '',
  'location': '',
  'description': '',
  'start': {
    'dateTime': '2022-10-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2022-10-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  #'recurrence': [
   # 'RRULE:FREQ=FREQ=DAILY;COUNT=2'
  #],
  #didn't implement recurring meetings
  'attendees': [
    {'email': 'test1@example.com'},
    {'email': 'test2@example.com'},
  ],
    #reminders are sending an email a day before and a popup 10 min before, can change
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

def datetime_to_ics(time):
    time2=[str(time.month),str(time.day),str(time.hour),str(time.minute),str(time.second)]
    for i in range(len(time2)):
        if len(time2[i]) == 1:
            time2[i] = "0"+time2[i]
    newtime=str(time.year)+"-"+time2[0]+"-"+time2[1]+"T"+time2[2]+":"+time2[3]+":"+time2[4]+"-07:00"
    return newtime
def generate_ics(meeting):
    #meeting is a MeetingTimeProposal
    event=event_template
    print(event)
    print(event["attendees"])
    event["summary"]="Scalander Test Event" #need to get an input here
    event["description"]="Testing Schedule Generation" #also need to get an input here
    #also need an input for location
    event["start"]["dateTime"] = datetime_to_ics(meeting.start)
    event["end"]["dateTime"] = datetime_to_ics(meeting.end)
    event["attendees"]=[]
    for i in range(len(meeting.commitedUsers)):
        email = meeting.commitedUsers[i].user.emails
        event["attendees"].append({"email":email})
    print(event)
    print(event["attendees"])
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

#notes:
# This code currently creates the meeting given as an input and adds it to the primary google calendar of whoever is running the code.
# If we run it for a user(e.g. website), it should add the meeting to the user's google calendar automatically
#
# I don't currently take inputs for title of meeting, description of meeting, or location, because I'm not sure how I can get them

