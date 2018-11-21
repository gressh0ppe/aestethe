import requests
import json
import re
import time
import api_keys as api


canvas_auth = api.canvas
slack_webhook = api.slack


def removeTags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text) # HTML-tag remover


class CanvasCourse:
    def __init__(self, course_id):
        self.course_id = course_id

        # Announcements
        self.id = "n/a"
        self.author = "n/a"
        self.posted = "n/a"
        self.url = "n/a"
        self.title = "n/a"
        self.message = "n/a"
        self.last_announcement = "n/a"

    def getLastAnnouncement(self):
        # Defines the URL for announcement
        announcements_url = "https://kristiania.instructure.com/api/v1/announcements"

        # Sends an API-request
        payload = {'access_token':canvas_auth, 'context_codes[]':'course_' + str(self.course_id)}
        r = requests.get(announcements_url, params=payload).json()

        # Assigns the data to their respective variables
        self.id = r[0]["id"]
        self.author = r[0]["user_name"].encode('utf-8')
        self.posted = r[0]["posted_at"].encode('utf-8')  # last reply at
        self.url = r[0]["url"].encode('utf-8')
        self.title = r[0]["title"].encode('utf-8')  # post title
        message_temp = r[0]["message"].encode('utf-8')  # message body
        self.message = removeTags(message_temp)  # removes eventual HTML-tags

        # Formats the output the message
        self.last_announcement = ("Postet av: " + self.author + "\nPostet: "+ self.posted + "\n\n" + self.message)


# Courses
klipp = CanvasCourse(1396)
fp1 = CanvasCourse(1236)
fp2 = CanvasCourse(1720)


fp1.getLastAnnouncement()
print(fp1.last_announcement)
