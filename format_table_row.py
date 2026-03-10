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


def _normalize_image_description(description: str) -> str:
    """Normalize certain common Wikipedia image captions to desired phrasing."""
    if not isinstance(description, str):
        return ""

    # Normalize known patterns like:
    #   "Barnard's Star is located in the constellation Ophiuchus."
    # to:
    #   "Location of Barnard's Star in the constellation Ophiuchus"
    m = re.match(r"^(.*) is located in the constellation (.+)\.?$", description)
    if m:
        subject, const = m.groups()
        return f"Location of {subject} in the constellation {const}"

    return description


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

def _resolve_image_url(src: str) -> str:
    """Normalize the image URL to an absolute form."""
    if not src:
        return ""
    src = src.strip()
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return "https://en.wikipedia.org" + src
    return src


def _resolve_image_url_from_srcset(srcset: str) -> str:
    """Pick a best-guess URL from a srcset attribute."""
    if not srcset:
        return ""
    parts = [p.strip() for p in srcset.split(",") if p.strip()]
    if not parts:
        return ""
    # Prefer the last entry (usually the highest resolution).
    best = parts[-1].split()[0]
    return _resolve_image_url(best)


def _caption_from_html_near_image(html: str, image_url: str) -> str:
    """Try to find a caption/text adjacent to an image in the raw HTML."""
    # Match by filename because full URL may be escaped or vary slightly.
    filename = image_url.split("/")[-1]
    idx = html.find(filename)
    if idx == -1:
        return ""

    # Search from the end of the img tag to the end of the container.
    start = html.rfind('<', 0, idx)
    end = html.find('</div>', idx)
    if end == -1:
        end = html.find('</td>', idx)
    snippet = html[start:end] if start != -1 and end != -1 else html[idx:idx + 500]

    # Strip tags but keep the plain text (e.g., caption after <br/>)
    text = re.sub(r"<[^>]+>", "", snippet)
    return _clean_text(text)


def getImages(link, session):
    """Return all images found on a Wikipedia page (with descriptive text)."""
    page = session.get(link)
    selector = Selector(page.content, url=link)

    # Restrict to the main content area to avoid icons/toolbar images.
    content = selector.find("div", id="mw-content-text")
    if content is None:
        content = selector

    page_html = page.text
    images = []
    seen_urls = set()

    def add_image(url: str, description: str):
        if not url or url in seen_urls:
            return
        description = _normalize_image_description(description)
        images.append({"url": url, "description": _clean_text(description)})
        seen_urls.add(url)

    # Capture images inside <figure> blocks (preferred source for captions).
    for figure in content.find_all("figure"):
        img = figure.find("img")
        if img is None:
            continue

        src = img.attrib.get("src") or img.attrib.get("data-src")
        if not src:
            src = _resolve_image_url_from_srcset(img.attrib.get("srcset", ""))
        url = _resolve_image_url(src)
        if not url:
            continue

        figcaption = figure.find("figcaption")
        description = figcaption.get_all_text() if figcaption is not None else ""
        if not description:
            description = _caption_from_html_near_image(page_html, url)

        add_image(url, description)

    # Capture images inside infobox tables (common for star pages).
    for infobox in content.find_all("table"):
        cls = infobox.attrib.get("class") or ""
        if "infobox" not in cls:
            continue

        # Prefer images inside thumbnail blocks within the infobox (these have captions).
        for thumb in infobox.find_all("div"):
            cls = thumb.attrib.get("class") or ""
            if "thumb" not in cls:
                continue

            img = thumb.find("img")
            if img is None:
                continue

            src = img.attrib.get("src") or img.attrib.get("data-src")
            if not src:
                src = _resolve_image_url_from_srcset(img.attrib.get("srcset", ""))
            url = _resolve_image_url(src)
            if not url:
                continue

            caption = ""
            caption_div = thumb.find("div", class_="thumbcaption")
            if caption_div is not None:
                caption = caption_div.get_all_text()
            else:
                caption = _caption_from_html_near_image(page_html, url)

            add_image(url, caption)

        # Then capture any remaining images inside the infobox (fallback to alt/title).
        for img in infobox.find_all("img"):
            src = img.attrib.get("src") or img.attrib.get("data-src")
            if not src:
                src = _resolve_image_url_from_srcset(img.attrib.get("srcset", ""))
            url = _resolve_image_url(src)
            if not url:
                continue

            if url in seen_urls:
                continue

            desc = ""
            if img.attrib.get("alt"):
                desc = img.attrib.get("alt")
            elif img.attrib.get("title"):
                desc = img.attrib.get("title")
            else:
                desc = _caption_from_html_near_image(page_html, url)

            add_image(url, desc)

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
    
    
            
            
