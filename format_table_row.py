
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
    # Ensure Wikipedia allows scraping by setting a realistic User-Agent
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    page = session.get(link)
    if page.status_code != 200:
        return []

    soup = BeautifulSoup(page.content, "html.parser")
    images = []

    # 1) Extract images inside infobox from either td.infobox-image or centered container
    infobox = soup.find("table", class_="infobox")
    if infobox:
        # infobox-image images
        infobox_image_imgs = infobox.select("td.infobox-image img")
        for img in infobox_image_imgs:
            td_parent = img.find_parent("td")
            if td_parent and "infobox-data" in td_parent.get("class", []):
                continue
            url = img.get("src") or img.get("data-src")
            if not url:
                continue
            url = formatURLImage(url)
            description = img.get("alt", "").strip()
            if not description:
                caption = img.find_parent("td")
                if caption:
                    description = caption.get_text(separator=" ", strip=True)
            images.append({"url": url, "description": description})

        # centered-image container images
        centered_containers = infobox.select("td div[style*='text-align: center;'][style*='margin-left:auto;'][style*='margin-right:auto']")
        for container in centered_containers:
            for img in container.find_all("img"):
                td_parent = img.find_parent("td")
                if td_parent and "infobox-data" in td_parent.get("class", []):
                    continue
                url = img.get("src") or img.get("data-src")
                if not url:
                    continue
                url = formatURLImage(url)
                description = img.get("alt", "").strip()
                if not description:
                    caption = img.find_parent("td")
                    if caption:
                        description = caption.get_text(separator=" ", strip=True)
                images.append({"url": url, "description": description})

    # 2) Extract all images inside figures
    figures = soup.find_all("figure")
    for figure in figures:
        img = figure.find("img")
        if not img:
            continue

        url = img.get("src") or img.get("data-src")
        if not url:
            continue
        url = formatURLImage(url)

        figcaption = figure.find("figcaption")
        description = ""
        if figcaption and figcaption.text.strip():
            description = figcaption.text.strip()
        else:
            description = img.get("alt", "").strip()

        images.append({"url": url, "description": description})

    # Deduplicate by url preserving first description
    seen = set()
    unique_images = []
    for img in images:
        if img["url"] in seen:
            continue
        seen.add(img["url"])
        unique_images.append(img)

    return unique_images

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
    
    
            
            
