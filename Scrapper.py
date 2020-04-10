from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen
import pandas as pd


loto_url = 'https://www.lldj.com/en/LatestResults/Loto'

req = Request(loto_url, headers={'User-Agent': 'Mozilla/5.0'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
draw_info = page_soup.find("input",{"id":"resultdateinput"})

draws = int(draw_info['value'])

loto_scrap = pd.DataFrame(columns = ['Draw Number','Jackpot','Date',"Ball 1","Ball 2","Ball 3","Ball 4","Ball 5","Ball 6","Extra Ball"])
for i in range(1,draws + 1):
    
    print("Draw #"+ str(i))
    my_url = 'https://www.lldj.com/en/LatestResults/Loto?draw='+str(i)

    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = uReq(req)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    draw_info = page_soup.findAll("span",{"class":"yellow"})
    draw_date = draw_info[0].text
    draw_date = draw_date.split(" ")
    draw_date = draw_date[3]
    draw_date = draw_date.split("/")
    draw_jackpot = draw_info[1].text
    day = draw_date[0]
    month = draw_date[1]
    year = draw_date[2]
    loto_balls_container = page_soup.findAll("ul",{"class":"list ballslist pseudoclear"})
    loto_balls = loto_balls_container[0].find_all("li")
    
    row = {
        'Draw Number': i,
        'Date': year + "-" + month + "-" + day,
        'Jackpot': draw_jackpot,
        'Ball 1': loto_balls[0].text,
        'Ball 2': loto_balls[1].text,
        'Ball 3': loto_balls[2].text,
        'Ball 4': loto_balls[3].text,
        'Ball 5': loto_balls[4].text,
        'Ball 6': loto_balls[5].text,
        'Extra Ball': loto_balls[6].text,
    }
    ser = pd.Series(row)
    loto_scrap = loto_scrap.append(ser,ignore_index=True)
    loto_scrap.to_csv('Loto_Scrap.csv',index = False)
loto_scrap