import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_nearest_stars_and_brown_dwarfs"

def printPage():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find('table', class_='mw-collapsible')
    trs = tables.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            print(td)
        # print('-------------------')
        # print(tds)
        # print('-------------------')
    #print(tables.prettify())
    return tables.prettify()
    