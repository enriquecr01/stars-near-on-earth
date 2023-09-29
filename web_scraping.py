import requests
from bs4 import BeautifulSoup
import json

from format_table_row import formatStar

URL = "https://en.wikipedia.org/wiki/List_of_nearest_stars_and_brown_dwarfs"

def printPage():
    # Scrapping
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find('table', class_='mw-collapsible')
    trs = tables.find_all('tr')
    
    # Formatting objects
    systemsFormatted = []
    
    
    for tr in trs:
        tds = tr.find_all('td')
        
        # if len(tds) == 5:
        #     print(len(tds), tr)
        
        if len(tds) == 10:
            star = processSingleStar(tds)
            systemsFormatted.append(star)
        starObject = {}
        # for td in enumerate(tds):
        #     # if len(tds) == 11: 
        #     # if len(tds) == 10: 
                
            
        #     if td[0] == 0:
        #         if 'colspan' in td[1].attrs:
        #             print("ahuievpo")
        #         else:
        #             print("no hay carnal")
                    
        #         if 'rowspan' in td[1].attrs:
        #             print("rowspan", td[1].attrs)
        #         else:
        #             print("no hay rowspan")
                    
                    
                    
        # print('-------------------')
        # print(tds)
        # print('-------------------')
    #print(tables.prettify())
    # print(json.dumps(systemsFormatted))
    # return tables.prettify()
    
    
    return json.dumps(systemsFormatted)
    
def processSingleStar(tds): 
    systemObject = { "systemName": "N/A"  }
    starObject = {}
    starsArray = []
    for td in enumerate(tds):
        propertyKey, objectFormatted, images = formatStar(td)
        if images != None:
            starObject['images'] = images
        starObject[propertyKey] = objectFormatted
    
    starsArray.append(starObject)
    systemObject["stars"] = starsArray
    return systemObject