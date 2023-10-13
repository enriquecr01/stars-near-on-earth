import requests
from bs4 import BeautifulSoup
import json
import requests

from format_table_row import formatStar, formatSystem, getImages, formatStarFiveTds, formatStarSixTds, formatStarSevenTds, formatStarNineTds, formatStarNineTdsWithConstelation

URL = "https://en.wikipedia.org/wiki/List_of_nearest_stars_and_brown_dwarfs"
session = requests.Session()


def printPage():
    # Scrapping
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find('table', class_='mw-collapsible')
    trs = tables.find_all('tr')
    
    # Formatting objects
    systemsFormatted = []
    
    # Common columns with the stars
    distance = 0
    constellation = ''
    coordinates = ''
    parallax = ''
    notes = ''
    
    for tr in trs:
        tds = tr.find_all('td')
        
        if len(tds) == 10:
            star = processSingleStar(tds)
            systemsFormatted.append(star)
            
        if len(tds) == 11:
            system = processSystemWithStars(tds)
            systemsFormatted.append(system)
            distance = system['stars'][0]["distance"]
            constellation = system['stars'][0]['constellation']
            coordinates = system['stars'][0]['coordinates']
            parallax = system['stars'][0]['stellarParallax']
            notes = system['stars'][0]['notes']
                    
        if len(tds) == 5:
            star = processStarWithFiveTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['coordinates'] = coordinates
            star['stellarParallax'] = parallax
            star['notes'] = notes
            systemsFormatted[len(systemsFormatted) - 1]['stars'].append(star)
            
        if len(tds) == 6:
            star = processStarWithSixTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            systemsFormatted[len(systemsFormatted) - 1]['stars'].append(star)
            
        if len(tds) == 7:
            star = processStarWithSevenTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            systemsFormatted[len(systemsFormatted) - 1]['stars'].append(star)
            
            
        if len(tds) == 9:
            hasConstellation = False

            for td in tds:        
                if td.attrs.get("style"):
                    if td.attrs["style"] == "background-color: pink":
                        hasConstellation = True

            
            if hasConstellation: 
                star = processSingleStar(tds)
                systemsFormatted.append(star)
            else:
                star = processStarWithNineTds(tds)
                star['distance'] = distance
                star['stellarParallax'] = parallax
                systemsFormatted[len(systemsFormatted) - 1]['stars'].append(star)
    
    return json.dumps(systemsFormatted)
    
def processSingleStar(tds): 
    systemObject = { "systemName": "N/A"  }
    starObject = {}
    starsArray = []
    for td in enumerate(tds):
        propertyKey, objectFormatted, images = formatStar(td, session)
        if images != None:
            starObject['images'] = images
        starObject[propertyKey] = objectFormatted
    
    starsArray.append(starObject)
    systemObject["stars"] = starsArray
    return systemObject

def processSystemWithStars(tds): 
    systemObject = {}
    starObject = {}
    starsArray = []
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatSystem(td)
        if propertyKey == "systemName":
            systemObject[propertyKey] = objectFormatted
        else:
            starObject[propertyKey] = objectFormatted
            
            
    starLink = tds[1].find_all("a")
    hrefs = starLink
        
    if len(starLink) == 0:
        hrefs = tds[0].find_all("a")
            
    images = getImages("https://en.wikipedia.org" + hrefs[0].attrs["href"], session)
    
    starObject['images'] = images
    
    starsArray.append(starObject)
    systemObject["stars"] = starsArray
    return systemObject


def processStarWithFiveTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarFiveTds(td)
        starObject[propertyKey] = objectFormatted
            
    return starObject

def processStarWithSixTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarSixTds(td)
        starObject[propertyKey] = objectFormatted
            
    return starObject


def processStarWithSevenTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarSevenTds(td)
        starObject[propertyKey] = objectFormatted
            
    return starObject

def processStarWithNineTds(tds):
    starObject = {}
    for td in enumerate(tds):

        propertyKey, objectFormatted = formatStarNineTds(td)
        starObject[propertyKey] = objectFormatted
            
    return starObject