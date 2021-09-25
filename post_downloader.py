import requests
from time import sleep
from bs4 import BeautifulSoup
import json
import re
from pprint import pprint

base='https://www.investorvillage.com'
postUrl = 'https://www.investorvillage.com/smbd.asp?mb=155&mn=8&pt=msg&mid=15747'

pattern = re.compile('In response to')

with open('updated_data.json','r',encoding="utf-8") as jd:
    data = json.load(jd)


def get_id():
    with open('post_failed_id.txt', "r",encoding="utf-8") as file:
        return int(file.readlines()[0])

def get_post(pid):
    if pid not in data:
        print(f'No post with id {pid}')
        return
    if 'parent' not in data[pid].keys():
        print(f'Processing post {pid}')
    else:
        return
    try:
        r = requests.get(data[pid]['link'])
        soup = BeautifulSoup(r.content, features="html.parser")
        parent = soup.findAll('img', {'class':'rszImgExpandMsg'})
        if len(parent)>0:
            data[pid]['parent'] = [t.parent.find('a').get_text(strip=True).replace('msg ','') for t in parent][0]
        else:
            data[pid]['parent'] = "-1"
        data[pid]['post'] = soup.find('div', {"id":"divMessageText"}).get_text(strip=True)
        # pprint([t.parent.find('a').get_text(strip=True).replace('msg ','') for t in soup.findAll('img', {'class':'rszImgExpandMsg'})])
        # print(soup.find('div', {"id":"divMessageText"}).get_text(strip=True))
        save()
    except:
        print(f'Failed on postId {pid}, saving data loaded in memory...')
        save()
        with open('post_failed_id.txt', "w",encoding="utf-8") as file:
            file.write(pid)

def save():
    with open('updated_data.json', "w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)

postId = get_id()
while postId<12258:
    # print(f'Loading post {postId}')
    get_post(str(postId))
    # sleep(1)
    postId+=1