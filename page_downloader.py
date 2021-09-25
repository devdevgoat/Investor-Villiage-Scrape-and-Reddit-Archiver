import requests
from time import sleep
from bs4 import BeautifulSoup


page_id=1206




def get_page(pid):
    print(f'Getting page {pid}...')
    base='https://www.investorvillage.com/smbd.asp?'
    options='UseArchive='
    options+='&v=1'
    options+='&category=A'
    options+='&dValue='
    options+='&rValue='
    options+='&nmValue='
    options+='&pmValue='
    options+='&nhValue='
    options+=f'&MLPage={pid}'
    options+='&PrevNext=0'
    options+='&NewCount='
    options+='&pt=m'
    options+='&mb=155'
    options+='&SearchFor='
    options+='&Subject='
    options+='&DatePostedMin='
    options+='&DatePostedMax='
    options+='&RecommendedBy='
    options+='&AuthoredBy='
    options+='&MinRecs=0'
    options+='&FilterType='
    
    print(f'Loading url:')
    print(f'    {base}{options}')
    r = requests.get(f"{base}{options}")
    soup = BeautifulSoup(r.content)
    with open(f"{pid}.html", "w",encoding="utf-8") as file:
        file.write(str(soup))

def loop_pages(pid):
    print('Starting loop_pages')
    while pid>0:
        try:
            get_page(pid)
            pid-=1
            sleep(1)
        except:
            with open('failed_id.txt', "w",encoding="utf-8") as file:
                file.write(pid)
    print('Complete!')

with open('failed_id.txt', "r",encoding="utf-8") as file:
    page_id = int(file.readlines()[0])

print(f'Found page id {page_id}')
loop_pages(page_id)
