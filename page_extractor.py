import requests
from time import sleep
from bs4 import BeautifulSoup
import json

base='https://www.investorvillage.com'
page_id = 1207
data = {}

with open('ext_failed_id.txt', "r",encoding="utf-8") as file:
    page_id = int(file.readlines()[0])


def get_page(pid):
    print(f'Getting page {pid}.html...')
    with open(f'{pid}.html', "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features="html.parser")
    return soup

def extract_data(soup):
    print('extracting data')
    tmprows = soup.find("table", {"id": "tblMessages"}) #.find("tbody") #.find_all("tr")
    if tmprows.find("tbody") is not None:
        rows = tmprows.find("tbody").find_all("tr", class_="mmBoardUnselected")
    else:
        rows = tmprows.find_all("tr", class_="mmBoardUnselected")
    # print(rows)
    for row in rows:
        cells = row.find_all("td")
        msgId = cells[1].get_text()
        data[msgId] = {}
        data[msgId]['subject'] = cells[3].get_text(strip=True)
        data[msgId]['author'] = cells[5].get_text(strip=True)
        data[msgId]['data'] = cells[8].get_text(strip=True)
        data[msgId]['link'] = f"{base}{cells[3].a['href']}"
        # cells[0].get_text()
        # and so on
        # print(f'{msgId}:{data[msgId]}')
    # print(data)

def loop_pages(pid):
    print('Starting loop_pages')
    while pid>0:
        try:
            soup = get_page(pid)
            extract_data(soup)
            pid-=1
        except:
            with open('ext_failed_id.txt', "w",encoding="utf-8") as file:
                file.write(str(pid))
    
    print('Loaded all pages to memory. writing file')
    try:
        with open('data.json', "w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)
    except:
        print(json.dumps(data,indent=4))

loop_pages(page_id)
# soup = get_page(page_id)
# extract_data(soup)