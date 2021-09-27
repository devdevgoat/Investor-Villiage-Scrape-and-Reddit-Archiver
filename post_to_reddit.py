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
    user_agent="simple archiver app by u/devdevgoat",
)
print(f'Logged in as {reddit.user.me()}')

reddit.validate_on_submit = True
subreddit = reddit.subreddit("CMKMArchive2")

def create_posts(fromFile, fromId):
    jd = load_file(fromFile)
    for i in jd:
        if int(i) <= fromId:
            print(f'skipping {i}...')
            continue
        title = f"{jd[i]['data']} | {jd[i]['subject']}"
        selftext  = f"{jd[i]['post']}"
        if len(selftext)>4000:
            selftext = selftext[:3000] + "...\n\n [Truncated due to reddit comment length. See source link for original. Backed up on git as well."
        selftext += "\n\n---\n\n"
        selftext = selftext.replace("Jump to msg. #"," Jump to msg. \n\n#")
        selftext = selftext.replace("- - - - -By:"," \n\n---\n\nBy:")
        selftext += f"{jd[i]['data']} | {jd[i]['author']} | [Source]({jd[i]['link']} | JSON ID: {i})"
        thisPost = reddit.subreddit("CMKMArchive").submit(title, selftext=selftext)
        # savemodlog(thisPost.id)
        for r in jd[i]['replies']:
            makeReply(thisPost, jd[i]['replies'][r])
        save(i)
        print(f'posted {i}')

def makeReply(target, reply):
    selftext = f"{reply['post']}"
    if len(selftext)>10000:
            selftext = selftext[:9000] + "...\n\n [Truncated due to reddit comment length. See source link for original. Backed up on git as well."
    selftext += "\n\n---\n\n"
    selftext +=f"{reply['data']} | {reply['author']} | [Source]({reply['link']})"
    thisComment = target.reply(selftext)
    if 'replies' in reply:
        for r in reply['replies']:
            makeReply(thisComment, reply['replies'][r])

def save(data):
    with open('post_log.txt', "w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)
def savemodlog(sub):
    with open('mod_log_sub.txt', "ab",encoding="utf-8") as file:
            json.dump(f'\n{sub}',file,indent=4)
            

create_posts('nested_data_sorted.json', 0)