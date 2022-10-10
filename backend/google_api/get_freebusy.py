#for getting the freebusy status from the user
#############
# USAGE:
# run get_freebusy() and pass in the following:
# query_min is a datetime date object in format %Y-%m%d or a datetime.date object (needs to have year, month, and day) - this is the first day to query for freebusy information (default is today)
# query_max is a datetime date object in format %Y-%m%d or a datetime.date object (needs to have year, month, and day) - this is the last day to query for freebusy information (default is 7 days from today)
# NOTE: calendar MUST BE PUBLIC in order to get freebusy this way - will create a workaround eventually (using calendar secret id)
#############
from distutils.command.build_scripts import build_scripts
import os
# from time import strftime
from dotenv import load_dotenv
import datetime
from datetime import timedelta, date
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.http import request
import google.oauth2.credentials
import google_auth_oauthlib.flow

    
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"])
flow.redirect_uri = "https://localhost:8080/"
auth_uri = flow.authorization_url()
print("URI",auth_uri)
auth_request = redirect(flow.redirect_uri)
auth_response = auth_request.build_absolute_uri()
flow.fetch_token(authorization_response = auth_response)

tzoffset = "-07:00" #timezone offset - assumimg its PDT for now
today = date.today()
cal_ids = [{"id": "s603jfdbhtfn4fd50bkm7vqg3c@group.calendar.google.com"}, {"id": "30jid79sjfm4ofnih7n030mm0k@group.calendar.google.com"}] #for storing the user's calendar ids - hardcoded to test will be user input
formatted_ids = [] #for storing the calendar IDs in the format that query() takes
query_min = today.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset  #eariliest date-time to check for freebusy - default is midnight 1 week from today (as specified by RFC3339 https://www.rfc-editor.org/rfc/rfc3339#section-5.6)
query_max = (today + datetime.timedelta(days = 7)).strftime("%Y-%m-%d") + "T00:00:00" +tzoffset #latest date-time to check - default is midnight today, see query_max
commitments = []

# handling the calendar.list return data
def format_all(cals): #takes in a list of the user's calendars - default is all
    #takes in a set of the user's calendars from the google api and formats and returns them to be used in a freebusy query - use send_query()
    for cal in cals: #appends all calendar IDs to cal_id
        cal_ids.append(cal["id"])

    for id in cal_ids: #adds calendar IDs to formatted_ids in the format needed in query body
        formatted_ids.append({
            "id": id
        })
    return(formatted_ids)


def make_query(formatted_ids = cal_ids, query_max = query_max, query_min = query_min):
    # print(type(formatted_ids), type(query_min), type(query_max)) #TODO: remove
    if type(query_min) == datetime.date:
        q_min = query_min.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset
    else:
        q_min = query_min
    if type(query_max) == datetime.date:
        q_max = query_max.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset
    else:
        q_max = query_max
    query_body = {
        # "calendarExpansionMax": 50, # Maximal number of calendars for which FreeBusy information is to be provided. Optional. Maximum value is 50.
        # "groupExpansionMax": 50, # Maximal number of calendar identifiers to be provided for a single group. Optional. An error is returned for a group with more members than this value. Maximum value is 100.
        "timeMax": q_max, # The end of the interval for the query formatted as per RFC3339. default is 1 week from today
        "items": formatted_ids, #IDs of the user's calendars - use format_all() to get these
        "timeMin": q_min, # The start of the interval for the query formatted as per RFC3339. default is today
        # "timeZone": "UTC", # Time zone used in the response. Optional. The default is UTC.
    #structure for query body from: https://google-api-client-libraries.appspot.com/documentation/calendar/v3/python/latest/calendar_v3.freebusy.html
    }
    return (query_body)

def send_commitments(freebusy):
    #gets the busy time blocks from the api response - takes in the api response
    to_check = []
    # print("FREEBUSY", freebusy)
    queried_cals = freebusy["calendars"]
    to_check = list(queried_cals.keys())
    # print("CHECK", to_check)
            
        # start = datetime.datetime.strptime(commitment["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
        # end = datetime.datetime.strptime(commitment["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
    for commitment in to_check:
        response_cal = queried_cals[commitment]
        busy_list = response_cal["busy"]
        # print("BUSY", busy_list)
        for event in busy_list:
            # print("EVENT", event)
            utc_start = datetime.datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
            utc_end = datetime.datetime.strptime(event["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
            naive_start = utc_start.replace(tzinfo=None) 
            naive_end = utc_end.replace(tzinfo=None) #makes start and end into naive objects...
            start = naive_start + datetime.timedelta(hours=-7)
            end = naive_end + datetime.timedelta(hours=-7) #...and manually shifts them to PST (ignores daylight savings)
            #TODO: make timezones work
            # print ("TYPES", type(start), type(end))
            commitments.append({
                "start": start,
                "end": end,
                "isAbsolute": True #can't really be sure from freebusy so we assume true
            })
    return(commitments)


def send_request(body): #google api things
    load_dotenv()
    service = build("calendar", "v3", developerKey=os.getenv("GOOGLE_API_KEY"))
    freebusy_collection = service.freebusy()
    calendar_collection = service.calendarList()
    calendar = calendar_collection.list() #gets the list of calendars that the user is subscribed to as a dictionary
    calendar_response = calendar.execute() #TODO: make it build with oauth key for this
    calendar_list = format_all(calendar_response)
    request_body = body
    request = freebusy_collection.query(body = request_body)
    # print("BODY: ",request_body, "REQUEST: ", request)
    response = request.execute()
    # print("RESPONSE", response)
    service.close()
    return(response)

#final product - RUN THIS
def get_freebusy(cal_ids = cal_ids, query_min = query_min, query_max = query_max): 
    #does all the things - 
    #takes datetime.date object or string "Y-m-d" for query min and max - takes from midnight to midnight on both dates (defualt is today and 1 week from today)
    # ids = format_all(cals)
    body = make_query(cal_ids, query_max, query_min)
    query = send_request(body)
    # print("QUERY", query)
    commitments = send_commitments(query)
    return (commitments)

print("RESULT: ", get_freebusy(query_min, query_max))