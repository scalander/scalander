#for getting the freebusy status from the user
#############
# USAGE:
# run get_freebusy() and pass in the following:
# query_min is a datetime date object in format %Y-%m%d - this is the first day to query for freebusy information (default is today)
# query_max is a datetime date object in format %Y-%m%d - this is the last day to query for freebusy information (default is 7 days from today)
# ids is a list of calendar ids (strings) that will specify which calendars to query (optional - defualt is all)
#############
#TODO: figure out how to test this
from calendar_api.calendar_api import google_calendar_api
import json
import os
from dotenv import load_dotenv
import datetime
from datetime import date
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from django.shortcuts import redirect

#google api things
load_dotenv()
service = build("calendar", "v3", developerKey=os.getenv("GOOGLE_API_KEY"))
freebusy_collection = service.freebusy()
calendar_collection = service.calendarList()
calendar = calendar_collection.list() #gets the list of calendars that the user is subscribed to as a dictionary

today = date.today()
g = google_calendar_api()
cal_ids = [{"id": "s603jfdbhtfn4fd50bkm7vqg3c@group.calendar.google.com"}, {"id": "30jid79sjfm4ofnih7n030mm0k@group.calendar.google.com"}] #for storing the user's calendar ids - hardcoded to test will be user input
formatted_ids = [] #for storing the calendar IDs in the format that query() takes
query_min = today.strftime("%Y-%m-%d") + "T00:00:00z"  #latest date-time to check for freebusy - default is midnight 1 week from today (as specified by RFC3339 https://www.rfc-editor.org/rfc/rfc3339#section-5.6)
query_max = (today + datetime.timedelta(days = 7)).strftime("%Y-%m-%d") + "T00:00:00z" #eariliest date-time to check - default is midnight today, see query_max
commitments = []

#sending/handling the query data
# def format_all(cals = calendar): #takes in a list of the user's calendars - default is all
#     #takes in a set of the user's calendars from the google api and formats and returns them to be used in a freebusy query - use send_query()
#     for cal in cals: #appends all calendar IDs to cal_id
#         cal_ids.append(cal["id"])

#     for id in cal_ids: #adds calendar IDs to formatted_ids in the format needed in query body
#         formatted_ids.append({
#             "id": id
#         })
#     return(formatted_ids)


def make_query(formatted_ids = cal_ids, query_max = query_max, query_min = query_min):
    # print(type(formatted_ids), type(query_min), type(query_max)) #TODO: remove
    query_body = {
        # "calendarExpansionMax": 50, # Maximal number of calendars for which FreeBusy information is to be provided. Optional. Maximum value is 50.
        # "groupExpansionMax": 50, # Maximal number of calendar identifiers to be provided for a single group. Optional. An error is returned for a group with more members than this value. Maximum value is 100.
        "timeMax": query_max, # The end of the interval for the query formatted as per RFC3339. default is 1 week from today
        "items": formatted_ids, #IDs of the user's calendars - use format_all() to get these
        "timeMin": query_min, # The start of the interval for the query formatted as per RFC3339. default is today
        # "timeZone": "UTC", # Time zone used in the response. Optional. The default is UTC.
    #structure for query body from: https://google-api-client-libraries.appspot.com/documentation/calendar/v3/python/latest/calendar_v3.freebusy.html
    }
    return (query_body)

def send_commitments(freebusy):
    print("FREEBUSY", freebusy)
    queried_cals = freebusy["calendars"]
    for cal in queried_cals:
        for commitment in cal["busy"]:
            # start = datetime.datetime.strptime(commitment["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
            # end = datetime.datetime.strptime(commitment["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
            start = commitment["start"]
            end = commitment["end"]
            
            commitments.append({
                "start": start,
                "end": end,
                "isAbsolute": True #can't really be sure from freebusy so we assume true
            })
    return(commitments)

#more google api things
request_body = make_query(cal_ids, query_max, query_min)
request = freebusy_collection.query(body = request_body)
print("BODY: ",request_body, "REQUEST: ", request)
response = request.execute()
service.close()

#final product - RUN THIS
def get_freebusy( query_min = query_min, query_max = query_max, cals = calendar): 
    #does all the things - 
    #takes datetime object Y-m-d for query min and max (defualt is today and 1 week from today) and calendar ids for cals (optional - default is all)
    # ids = format_all(cals)
    query = response
    print("QUERY", query)
    commitments = send_commitments(query)
    return (commitments)

print("RESULT: ", get_freebusy(query_min,query_max))