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
    username=os.getenv('MODUSER'),
    password=os.getenv('MODPASS'),
    user_agent="simple archive deleter app by u/devdevgoat",
)
print(f'Logged in as {reddit.user.me()}')


i = 10
while i>1:
    i=1
    # for item in reddit.subreddit("CMKMArchive").mod.unmoderated():
    for item in reddit.subreddit("CMKMArchive").mod.unmoderated():
        print(item)
        item.mod.approve()
        i+=1