import requests
import json
import re
import time
import announcement_msg_payload as amp
import api_keys as api


canvasAuth = api.canvas
slackWebHook = api.slack


lastID = -1;
# Function for removing HTML-tags
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text) # HTML-tag remover


# Looks for new announcement
def getAnnouncement(canvasAuth):
    # Defines the URL for announcements + payload
    announcementsURL = "https://kristiania.instructure.com/api/v1/announcements"
    payload = {'access_token':canvasAuth, 'context_codes[]':'course_1396'}

    # Requests the announcements
    r = requests.get(announcementsURL, params=payload).json()

    # Parses the required information
    aID = r[0]["id"]
    aPostedBy = r[0]["user_name"].encode('utf-8')
    aPostedAt = r[0]["posted_at"].encode('utf-8')  # last reply at
    aUrl = r[0]["url"].encode('utf-8')
    aTitle = r[0]["title"].encode('utf-8')  # post title
    _aMessage = r[0]["message"].encode('utf-8')  # message body
    aMessage = remove_tags(_aMessage)  # removes eventual HTML-tags

    # Formats the output the message
    announcement = ("Postet av: " + aPostedBy + "\nPostet: "+ aPostedAt + "\n\n" + aMessage)
    return aID, aUrl, aTitle, announcement


def post(slackWebHook, payload):
    data = json.dumps(payload)
    r = requests.post(slackWebHook, data = data, headers = {'Content-Type': 'application/json'})
    print(r.status_code)
    print(r.content)







# Prints latest announcement
#while True:
aID, aUrl, aTitle, announcement = getAnnouncement(canvasAuth)  # gets announcement and ID from func

payload = amp
#if (aID != lastID):  # checks if there's a new message
post(slackWebHook, payload)  # prints it if it is
#    lastID = aID  # assigns the last ID to variable to check against later

#time.sleep(5)  # sets the interval for checking for new announcements
