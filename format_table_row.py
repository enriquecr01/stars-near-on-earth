import re
import requests
from collections.abc import Iterable

from scrapling import Selector


def _clean_text(text: str) -> str:
    """Normalize text extracted from HTML cells."""
    if not isinstance(text, str):
        return ""

    # Normalize whitespace and remove non-breaking spaces
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()

    # Strip common wikipedia reference markers like [1], [a], etc.
    text = re.sub(r"\s*\[[^\]]*\]", "", text)

    # Strip trailing punctuation / markers (e.g. '$', '†', '#')
    text = re.sub(r"[‡†*#\$]+$", "", text).strip()

    return text


def _get_cell_text(cell):
    """Return the human-visible text for a cell (Selector or similar)."""
    if hasattr(cell, "get_all_text"):
        return _clean_text(cell.get_all_text())
    if hasattr(cell, "text"):
        return _clean_text(cell.text)
    return ""


def formatStar(tdNumber, session):
    # Columns in the Wikipedia table:
    # 0: Star name
    # 1: Minimum distance (ly)
    # 2: Date of approach (kyr)
    # 3: Current distance (ly)
    # 4: Stellar classification
    # 5: Mass (M☉)
    # 6: Apparent magnitude
    # 7: Constellation
    # 8: Right ascension
    # 9: Declination
    if tdNumber[0] == 0:
        hrefs = tdNumber[1].find_all("a")
        images = getImages("https://en.wikipedia.org" + hrefs[0].attrib["href"], session)
        return "name", _get_cell_text(tdNumber[1]), images
    if tdNumber[0] == 1:
        return "distance", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 2:
        return "notes", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 3:
        return "stellarParallax", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 4:
        return "stellarClass", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 5:
        return "solarMass", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 6:
        return "apparentMagnitude", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 7:
        return "constellation", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 8:
        return "coordinates", _get_cell_text(tdNumber[1]), None
    if tdNumber[0] == 9:
        return "notes", _get_cell_text(tdNumber[1]), None
    return "none", 0, None

def formatSystem(tdNumber):
    if tdNumber[0] == 0:
        return "systemName", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "distance", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "constellation", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 7:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 8:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 9:
        return "stellarParallax", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 10:
        return "notes", _get_cell_text(tdNumber[1])
    return "none", 0

def formatStarFiveTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "notes", _get_cell_text(tdNumber[1])
    return "none", 0

def formatStarSixTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "notes", _get_cell_text(tdNumber[1])
    return "none", 0

def formatStarSevenTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "notes", _get_cell_text(tdNumber[1])
    return "none", 0

def formatStarNineTds(tdNumber):
    if tdNumber[0] == 0:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "distance", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 7:
        return "stellarParallax", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 8:
        return "notes", _get_cell_text(tdNumber[1])
    return "none", 0

def formatStarNineTdsWithConstelation(tdNumber):
    if tdNumber[0] == 0:
        return "name", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 1:
        return "distance", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 2:
        return "constellation", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 3:
        return "coordinates", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 4:
        return "stellarClass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 5:
        return "solarMass", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 6:
        return "apparentMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 7:
        return "absoluteMagnitude", _get_cell_text(tdNumber[1])
    if tdNumber[0] == 8:
        return "stellarParallax", _get_cell_text(tdNumber[1])
    return "none", 0

def getImages(link, session):
    page = session.get(link)
    selector = Selector(page.content, url=link)
    figures = selector.find_all("figure")
    images = []

    mainTable = selector.find("table", class_="infobox")
    if mainTable is None:
        return images

    tds = mainTable.find("td")
    if tds is None:
        return images

    divFigures = tds.find(
        "div",
        {"style": "text-align: center; margin-left:auto; margin-right:auto"},
    )

    if divFigures is not None:
        divLocMap = divFigures.find(
            "div",
            class_="locmap",
        )

        if divLocMap is not None:
            imgs = divLocMap.find('img')
            divDesc = tds.find(
                "div",
                {"style": "padding-top:0.2em"},
            )
            image = {}
            if divDesc is None:
                image['description'] = divFigures.get_all_text().strip()
            else:
                image['description'] = divDesc.get_all_text().strip()

            if imgs is not None and imgs.attrib.get('src'):
                image['url'] = formatURLImage(imgs.attrib['src'])
                images.append(image)

        if divLocMap is None:
            if isinstance(divFigures, Iterable):
                for div in divFigures:
                    image = {}
                    divImgs = div.find("img")
                    if divImgs is not None and divImgs != -1 and divImgs.attrib.get('src'):
                        image['description'] = mainTable.find("tr").get_all_text().strip()
                        image['url'] = formatURLImage(divImgs.attrib['src'])
                        images.append(image)

    if figures is not None:
        for figure in figures:
            image = {}
            figcaption = figure.find('figcaption')
            imgs = figure.find('img')
            if imgs is not None and imgs.attrib.get('src'):
                image['description'] = figcaption.get_all_text().strip() if figcaption is not None else ""
                image['url'] = formatURLImage(imgs.attrib['src'])
                images.append(image)

    divLocMapMainTable = mainTable.find("div", class_="locmap")
    if divLocMapMainTable is not None:
        imgs = divLocMapMainTable.find('img')
        divDesc = divLocMapMainTable.find("div", {"style": "padding-top:0.2em"},)
        image = {}

        image['description'] = divDesc.get_all_text().strip() if divDesc is not None else divLocMapMainTable.get_all_text().strip()

        if imgs is not None and imgs.attrib.get('src'):
            image['url'] = formatURLImage(imgs.attrib['src'])
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
    
    
            
            
