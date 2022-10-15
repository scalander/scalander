#for getting the freebusy status from the user
#############
# USAGE:
# run get_freebusy() and pass in the following:
# query_min is a datetime date object in format %Y-%m%d or a datetime.date object (needs to have year, month, and day) - this is the first day to query for freebusy information (default is today)
# query_max is a datetime date object in format %Y-%m%d or a datetime.date object (needs to have year, month, and day) - this is the last day to query for freebusy information (default is 7 days from today)
# auth_code is a string gotten from the google api when the user consents - required (will spit out an assertion error)
# 
# example usage: get_freebusy("2022-10-09", "2022-10-10", "ya29.a0Aa4xrXOxt9h5nJCON0Fb3w0ACK3-t0FWfXzwFwF3RzASc-PXn2GN4UkJcuZOzcvJfvrqzOwcOKJzwxJ55mjlHAvYdQZLc6LXJpsCs-KmJXuljw8-XwcCZ3YRM-Jz6jQmBqXs80Wudghg7VHXSzqJhSS5b7KkaCgYKATASARASFQEjDvL9FFkGmCmFA7dRV_bEjGUrcg0163")
#############
import datetime
from datetime import timedelta, date
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# NOTE: this first comment block is depreciated code - is now being done in the frontend
# flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#     'client_secret.json',
#     scopes = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"])
# flow.redirect_uri = "https://localhost:8080/"
# auth_uri = flow.authorization_url()
# print("URI",auth_uri)
# auth_request = redirect(flow.redirect_uri)
# auth_response = auth_request.build_absolute_uri()
# flow.fetch_token(authorization_response = auth_response)

tzoffset = "-07:00" #timezone offset - assumimg its PDT for now
today = date.today()
query_min = today.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset  #eariliest date-time to check for freebusy - default is midnight 1 week from today (as specified by RFC3339 https://www.rfc-editor.org/rfc/rfc3339#section-5.6)
query_max = (today + timedelta(days = 7)).strftime("%Y-%m-%d") + "T00:00:00" +tzoffset #latest date-time to check - default is midnight today, see query_max

# handling the calendar.list return data
def format_all(cals): #takes in a list of the user's calendars from send_request()
    #takes in a set of the user's calendars from the google api and formats and returns them to be used in a freebusy query - use send_query()
    formatted_ids = [] #for storing the calendar IDs in the format that query() takes
    cal_ids = []
    for cal in cals["items"]: #appends all calendar IDs to cal_id
        cal_ids.append(cal["id"])

    for id in cal_ids: #adds calendar IDs to formatted_ids in the format needed in query body
        formatted_ids.append({
            "id": id
        })
    return(formatted_ids)


def make_query(query_min, query_max):
    # print(type(formatted_ids), type(query_min), type(query_max)) #TODO: remove
    if type(query_min) == datetime.date:
        q_min = query_min.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset
    elif len(query_min) == 25:
        q_min = query_min
    elif len(query_min) == 19:
        q_min = query_min + tzoffset
    elif len(query_min) == 10:
        q_min = query_min + "T00:00:00" +tzoffset
    else:
        raise Exception ("invalid query_min format")

    if type(query_max) == datetime.date:
        q_max = query_max.strftime("%Y-%m-%d") + "T00:00:00" +tzoffset
    elif len(query_max) == 25:
        q_max = query_max
    elif len(query_max) == 19:
        q_max = query_max
    elif len(query_max) == 10:
        q_max = query_max + "T00:00:00" +tzoffset
    else:
        raise Exception ("invalid query_max format")

    assert datetime.datetime.strptime(q_min, "%Y-%m-%dT00:00:00-07:00") < datetime.datetime.strptime(q_max, "%Y-%m-%dT00:00:00-07:00"), "query interval ends before it starts"

    # print(query_min,query_max)
    query_body = {
        # "calendarExpansionMax": 50, # Maximal number of calendars for which FreeBusy information is to be provided. Optional. Maximum value is 50.
        # "groupExpansionMax": 50, # Maximal number of calendar identifiers to be provided for a single group. Optional. An error is returned for a group with more members than this value. Maximum value is 100.
        "timeMax": q_max, # The end of the interval for the query formatted as per RFC3339. default is 1 week from today
        "items": "", #IDs of the user's calendars - will be added in send_request
        "timeMin": q_min, # The start of the interval for the query formatted as per RFC3339. default is today
        # "timeZone": "UTC", # Time zone used in the response. Optional. The default is UTC.
    #structure for query body from: https://google-api-client-libraries.appspot.com/documentation/calendar/v3/python/latest/calendar_v3.freebusy.html
    }
    return (query_body)

def send_commitments(freebusy, calendar_names):
    #gets the busy time blocks from the api response - takes in the api response
    to_check = []
    # print("FREEBUSY", freebusy)
    queried_cals = freebusy["calendars"]
    to_check = list(queried_cals.keys())
    busy_list = []
    sorted_commitments = {} #stores the commitments grouped by calendar
    formatted_commitments = {} #stores the commitments from sorted as commitment objects, and then adds calendar names
    # print("CHECK", to_check)
            
        # start = datetime.datetime.strptime(commitment["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
        # end = datetime.datetime.strptime(commitment["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
    for cal in to_check: #for each calendar in the response...
        commitments = []
        response_cal = queried_cals[cal]
        busy_list.clear()
        for busy in response_cal["busy"]: #for each commitment in the calendar...
            busy_list.append(busy)
        # print("BUSY:", busy_list)
        sorted_commitments[cal] = busy_list #add a calendarid:[commitments] to sorted_commitments
        # print ("SORTED:", sorted_commitments)
        
        # make the commitments into commitment objects:
        for calendar in to_check:
            commitments.clear()
            cals = queried_cals[calendar]
            for event in cals["busy"]:
                # print(event,calendar)
                utc_start = datetime.datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
                utc_end = datetime.datetime.strptime(event["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
                naive_start = utc_start.replace(tzinfo=None) 
                naive_end = utc_end.replace(tzinfo=None) #makes start and end into naive objects...
                start = naive_start + datetime.timedelta(hours=-7)
                end = naive_end + datetime.timedelta(hours=-7) #...and manually shifts them to PDT (ignores daylight savings)
                #TODO: make timezones work
                # print ("TYPES", type(start), type(end))
                commitments.append({
                    "start": start,
                    "end": end,
                    "isAbsolute": True #can't really be sure from freebusy so we assume true
                })
            formatted_commitments[calendar] = {}
            formatted_commitments[calendar]["busy"]= commitments
            calendar_name = calendar_names[calendar]
            formatted_commitments[calendar]["calendar_name"]= calendar_name
    # print(formatted_commitments)
    return(formatted_commitments)


def link_names(api_response):
    calendar_names = {} #stores calendars in the form id: name
    calendars = api_response["items"]
    for calendar in calendars:
        calendar_names[calendar["id"]] = calendar["summary"]
    return(calendar_names)

def send_request(body, code): #google api things
    service = build("calendar", "v3", credentials=Credentials(code))
    calendar_collection = service.calendarList()
    calendar_request = calendar_collection.list() #gets the list of calendars that the user is subscribed to as a dictionary
    calendar_response = calendar_request.execute()
    # print (calendar_response) #for name: get celendar_response.items.foreach.summary
    calendar_list = format_all(calendar_response)
    calendar_names = link_names(calendar_response)
    #TODO: this is returning an empty string at the start - fix
    assert calendar_list, "missing calendar.list() response or format_all() failed"
    body["items"] = calendar_list
    freebusy_request_body = body
    freebusy_collection = service.freebusy()
    freebusy_request = freebusy_collection.query(body = freebusy_request_body)
    # print("BODY: ",request_body, "REQUEST: ", request)
    response = freebusy_request.execute()
    # print("RESPONSE", response)
    service.close()
    # print("NAMES:", calendar_names)
    return(response, calendar_names)

#final product - RUN THIS
def get_freebusy(query_min = query_min, query_max = query_max, auth_code = ""): 
    #does all the things - 
    #takes datetime.date object or string "Y-m-d" for query min and max - takes from midnight to midnight on both dates (defualt is today and 1 week from today)
    #requires auth code from google api
    #example usage: get_freebusy("2022-10-09", "2022-10-10", "ya29.a0Aa4xrXOxt9h5nJCON0Fb3w0ACK3-t0FWfXzwFwF3RzASc-PXn2GN4UkJcuZOzcvJfvrqzOwcOKJzwxJ55mjlHAvYdQZLc6LXJpsCs-KmJXuljw8-XwcCZ3YRM-Jz6jQmBqXs80Wudghg7VHXSzqJhSS5b7KkaCgYKATASARASFQEjDvL9FFkGmCmFA7dRV_bEjGUrcg0163")
    assert auth_code != "", "missing auth code"
    # ids = format_all(cals)
    body = make_query(query_min, query_max)
    request = send_request(body, auth_code)
    query = request[0] #sets query equal to api response
    # print("QUERY", query)
    commitments = send_commitments(query, request[1])
    return (commitments)

#testing:
# print("RESULT: ", get_freebusy(auth_code="ya29.a0Aa4xrXPf7soIxP6p37Yr49umkFMtAHL5ajQanjrluDYCsBdHMGobWekgRDNj05QDgiCAxUlM2A8h_ICpZckbiLy9dBenBRa4pyg7LLbgEYRAJhxKzIPGv8CQd6AbEcg4SEvPVYH5BOPMnE3bJ59MFYd9hJy3MQaCgYKATASARASFQEjDvL9tz2eTsBmN_ajMrmGIfZjeA0165"))
