import os, json
import praw
from requests import Session
from dotenv import load_dotenv, find_dotenv

def load_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


session = Session()
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('SECRET'),
    username=os.getenv('BOTUSER'),
    password=os.getenv('BOTPASS'),
    user_agent="simple archive deleter app by u/devdevgoat",
)
print(f'Logged in as {reddit.user.me()}')

# import time
# current_timestamp = time.time()
# # 60 seconds * 60 minutes * 24 hours * 60 days = 2 months
# two_months_timestamp = current_timestamp - (60 * 60 * 24 * 60)
# query = 'timestamp:{}..{}'.format(current_timestamp, two_months_timestamp)
# results = reddit.subreddit('CMKMArchive').search(query, sort='new')

i=1
while i > 0: 
    print("looping")
    for s in reddit.subreddit('CMKMArchive').hot():
        print(s.title)
        s.delete()
        i+=1