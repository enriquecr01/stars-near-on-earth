import requests
from bs4 import BeautifulSoup
from collections.abc import Iterable


def formatStar(tdNumber, session):
    if tdNumber[0] == 0:
        hrefs = tdNumber[1].find_all("a")
        images = getImages("https://en.wikipedia.org" + hrefs[0].attrs["href"], session)
        return "name", tdNumber[1].text, images
    if tdNumber[0] == 1:
        return "distance", tdNumber[1].text, None
    if tdNumber[0] == 2:
        return "constellation", tdNumber[1].text, None
    if tdNumber[0] == 3:
        return "coordinates", tdNumber[1].text, None
    if tdNumber[0] == 4:
        return "stellarClass", tdNumber[1].text, None
    if tdNumber[0] == 5:
        return "solarMass", tdNumber[1].text, None
    if tdNumber[0] == 6:
        return "apparentMagnitude", tdNumber[1].text, None
    if tdNumber[0] == 7:
        return "absoluteMagnitude", tdNumber[1].text, None
    if tdNumber[0] == 8:
        return "stellarParallax", tdNumber[1].text, None
    if tdNumber[0] == 9:
        return "notes", tdNumber[1].text, None
    return "none", 0, None

def formatSystem(tdNumber):
    if tdNumber[0] == 0:
        return "systemName", tdNumber[1].text
    if tdNumber[0] == 1:
        return "name", tdNumber[1].text
    if tdNumber[0] == 2:
        return "distance", tdNumber[1].text
    if tdNumber[0] == 3:
        return "constellation", tdNumber[1].text
    if tdNumber[0] == 4:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 5:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 6:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 7:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 8:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 9:
        return "stellarParallax", tdNumber[1].text
    if tdNumber[0] == 10:
        return "notes", tdNumber[1].text
    return "none", 0

def formatStarFiveTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 2:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 3:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 4:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 5:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 6:
        return "notes", tdNumber[1].text
    return "none", 0

def formatStarSixTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 2:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 3:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 4:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 5:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 6:
        return "notes", tdNumber[1].text
    return "none", 0

def formatStarSevenTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 2:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 3:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 4:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 5:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 6:
        return "notes", tdNumber[1].text
    return "none", 0

def formatStarNineTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "distance", tdNumber[1].text
    if tdNumber[0] == 2:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 3:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 4:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 5:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 6:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 7:
        return "stellarParallax", tdNumber[1].text
    if tdNumber[0] == 8:
        return "notes", tdNumber[1].text
    return "none", 0

def formatStarNineTdsWithConstelation(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "distance", tdNumber[1].text
    if tdNumber[0] == 2:
        return "constellation", tdNumber[1].text
    if tdNumber[0] == 3:
        return "coordinates", tdNumber[1].text
    if tdNumber[0] == 4:
        return "stellarClass", tdNumber[1].text
    if tdNumber[0] == 5:
        return "solarMass", tdNumber[1].text
    if tdNumber[0] == 6:
        return "apparentMagnitude", tdNumber[1].text
    if tdNumber[0] == 7:
        return "absoluteMagnitude", tdNumber[1].text
    if tdNumber[0] == 8:
        return "stellarParallax", tdNumber[1].text
    return "none", 0

def getImages(link, session):
    page = session.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    figures = soup.findAll("figure")
    images = []
    # print("-------------" + link + "-----------------")

    mainTable = soup.find("table", class_="infobox")
    tds = mainTable.find("td")
    divFigures = tds.find(
        "div",
        attrs={"style": "text-align: center; margin-left:auto; margin-right:auto"},
    )
    
    if divFigures != None:
    
        divLocMap = divFigures.find(
            "div",
            class_="locmap",
        )
        
        if divLocMap != None:
            imgs = divLocMap.find('img')
            divDesc = tds.find(
                "div",
                attrs={"style": "padding-top:0.2em"},
            )
            image = {}
            if divDesc == None:
                image['description'] = divFigures.text
                
            if divDesc != None:
                image['description'] = divDesc.text.strip()
                
            image['url'] = formatURLImage(imgs.attrs['src'])
            images.append(image)
        
        if divLocMap == None:
            if isinstance(divFigures, Iterable):
                for div in divFigures:
                    image = {}
                    divImgs = div.find("img")
                    if divImgs != None and divImgs != -1:
                        image['description'] = div.text.strip()
                        image['url'] = formatURLImage(divImgs.attrs['src'])
                        images.append(image)

    if figures != None:
        for figure in figures:
            image = {}
            figcaption = figure.find('figcaption')
            imgs = figure.find('img')
            image['description'] = figcaption.text.strip()
            
            if imgs != None:
                image['url'] = formatURLImage(imgs.attrs['src'])
            
            images.append(image)
    
    return images

def formatURLImage(originalURL):
    if "thumb" not in originalURL:
        return originalURL
    
    splitedURL = originalURL.split("/")
    lastPartUrl = splitedURL[len(splitedURL) - 1]
    splitedLastPartUrl = lastPartUrl.split("-")
    splitedLastPartUrl.pop(0)
    del splitedURL[len(splitedURL) - 1]
    
    finalUrl = "/".join(splitedURL)
    
    lastPart = "-".join(splitedLastPartUrl)
    
    finalUrl += "/1200px-" + lastPart
    
    
    return finalUrl
    
    
            
            
