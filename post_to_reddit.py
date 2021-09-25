import os, json
import praw
from requests import Session
from dotenv import load_dotenv, find_dotenv

def load_file(file_name,fromId):
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
        for d in data:
            if d <= fromId:
                del data[d]
        return data


session = Session()
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('SECRET'),
    username=os.getenv('USER'),
    password=os.getenv('PASS'),
    user_agent="simple archiver app by u/devdevgoat",
)
print(f'Logged in as {reddit.user.me()}')

reddit.validate_on_submit = True
subreddit = reddit.subreddit("CMKMArchive")

def create_posts(fromFile):
    with open('post_log.txt', "r",encoding="utf-8") as file:
        fromId = file.readlines()[0]    
    print(f'loading from id {fromId}')
    jd = load_file(fromFile, fromId)
    for i in jd:
        title = f"{jd[i]['data']} | {jd[i]['subject']}"
        selftext  = f"{jd[i]['post']}"
        selftext += "\n\n---\n\n"
        selftext += f"{jd[i]['data']} | {jd[i]['author']} | [Source]({jd[i]['link']})"
        if len(selftext)>4000:
             selftext = selftext[:3000] + "...\n\n [Truncated due to reddit comment length. See source link for original. Backed up on git as well."
        thisPost = reddit.subreddit("CMKMArchive").submit(title, selftext=selftext)
        for r in jd[i]['replies']:
            makeReply(thisPost, jd[i]['replies'][r])
        save(i)

def makeReply(target, reply):
    selftext = f"{reply['post']}"
    selftext += "\n\n---\n\n"
    selftext +=f"{reply['data']} | {reply['author']} | [Source]({reply['link']})"
    thisComment = target.reply(selftext)
    if 'replies' in reply:
        for r in reply['replies']:
            makeReply(thisComment, reply['replies'][r])

def save(data):
    with open('post_log.txt', "w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)
            



create_posts('nested_data_sorted.json')