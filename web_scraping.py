import requests
from multiprocessing import Pool, cpu_count

from scrapling import Selector

from format_table_row import (
    _clean_text,
    formatStar,
    formatSystem,
    getImages,
    formatStarFiveTds,
    formatStarSixTds,
    formatStarSevenTds,
    formatStarNineTds,
    formatStarNineTdsWithConstelation,
)


def _get_cell_text(cell):
    """Extract visible text from a scrapling Selector cell."""
    if hasattr(cell, "get_all_text"):
        return _clean_text(cell.get_all_text())
    if hasattr(cell, "text"):
        return _clean_text(cell.text)
    return ""

URL = "https://en.wikipedia.org/wiki/List_of_nearest_stars_and_brown_dwarfs"
session = requests.Session()
# Use a realistic User-Agent to avoid being blocked by Wikipedia's anti-bot rules
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
})


def find_nearest_stars_table(selector):
    """Find the main table listing nearest stars.

    Uses a few fallbacks to be resilient against small HTML changes.
    """

    # Prefer the “known systems within 20 ly” table (so Sun / Solar System appears).
    for t in selector.find_all('table'):
        cap = t.find('caption')
        if cap and 'known systems within 20 light-years' in cap.get_all_text().lower():
            return t

    # Next, try to locate a table that looks like the “stars passing near Sun” table.
    for t in selector.find_all('table'):
        cls = (t.attrib.get('class') or "").lower()
        if 'wikitable' not in cls:
            continue

        headers = [th.get_all_text().strip().lower() for th in t.find_all('th')]
        if any('distance' in h for h in headers) and any('star name' in h or 'star' in h for h in headers):
            return t

    # Fallback: pick a wikitable with many rows
    for t in selector.find_all('table'):
        cls = (t.attrib.get('class') or "").lower()
        if 'wikitable' not in cls:
            continue
        if len(t.find_all('tr')) > 10:
            return t

    # Last resort: first table on the page
    return selector.find('table')


def parse_known_systems_within_20ly(selector):
    """Parse the "Known systems within 20 light-years" table (includes Sun)."""

    for t in selector.find_all('table'):
        cap = t.find('caption')
        if not cap or 'known systems within 20 light-years' not in cap.get_all_text().lower():
            continue

        systems = []
        trs = t.find_all('tr')
        # Skip header rows (usually first 2 rows)
        for tr in trs[2:]:
            tds = tr.find_all('td')
            if len(tds) < 9:
                continue

            systemName = _get_cell_text(tds[0])
            name = _get_cell_text(tds[1])
            distance = _get_cell_text(tds[2])
            stellarClass = _get_cell_text(tds[5])
            solarMass = _get_cell_text(tds[6])
            apparentMagnitude = _get_cell_text(tds[7])
            absoluteMagnitude = _get_cell_text(tds[8])
            stellarParallax = _get_cell_text(tds[9]) if len(tds) > 9 else ""
            notes = _get_cell_text(tds[10]) if len(tds) > 10 else ""

            star = {
                "name": name,
                "distance": distance,
                "stellarClass": stellarClass,
                "solarMass": solarMass,
                "apparentMagnitude": apparentMagnitude,
                "absoluteMagnitude": absoluteMagnitude,
                "stellarParallax": stellarParallax,
                "notes": notes,
                "images": _fetch_images_from_row(tds) or [],
            }
            systems.append({"systemName": systemName, "stars": [star]})

        return systems

    return []


def _fetch_images_from_row(tds):
    """Try to fetch images from the first /wiki/ link found in the given row."""
    for td in tds:
        for a in td.find_all("a"):
            href = a.attrib.get("href")
            if not href or not href.startswith("/wiki/"):
                continue
            try:
                imgs = getImages("https://en.wikipedia.org" + href, session)
                if imgs:
                    return imgs
            except Exception:
                continue
    return []


def printPage(use_multiprocessing: bool = False):
    # Scraping
    page = session.get(URL)
    selector = Selector(page.content, url=URL)

    # Primary table (stars passing near Sun)
    table = find_nearest_stars_table(selector)
    if table is None:
        raise RuntimeError("Unable to locate nearest stars table on page")

    trs = table.find_all('tr')

    result = []
    # Parse the detected table
    if use_multiprocessing and cpu_count() >= 4:
        print("Using Multiprocessing")
        trsString = [str(tr) for tr in trs]
        longitud = len(trsString) - 1
        point1 = longitud // 4
        point2 = 2 * longitud // 4
        point3 = 3 * longitud // 4
        part1 = trsString[:point1]
        part2 = trsString[point1:point2]
        part3 = trsString[point2:point3]
        part4 = trsString[point3:]
        arrays = [part1, part2, part3, part4]
        p = Pool()
        results = p.map(processAllTrsMultiprocessing, arrays)
        p.terminate()
        p.join()
        result = results[0] + results[1] + results[2] + results[3]
    else:
        print("Normal using")
        result = processAllTrs(trs)

    # Add Sun / Solar System if missing (from the known-systems table)
    known_systems = parse_known_systems_within_20ly(selector)
    existing_names = {star.get('name') for sys in result for star in sys.get('stars', []) if star.get('name')}
    for sys in known_systems:
        star = sys.get('stars', [])[0] if sys.get('stars') else None
        if star and star.get('name') not in existing_names:
            result.append(sys)
            existing_names.add(star.get('name'))

    return result
    
def processAllTrsMultiprocessing(trs):
    # Formatting objects
    systemsFormatted = []
    
    # Common columns with the stars
    distance = 0
    constellation = ''
    coordinates = ''
    parallax = ''
    notes = ''
    
    for tr in trs:
        trParsed = Selector(tr)
        
        tds = trParsed.find_all('td')
        
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
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
        if len(tds) == 6:
            star = processStarWithSixTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
            
        if len(tds) == 7:
            star = processStarWithSevenTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
            
            
        if len(tds) == 9:
            hasConstellation = False

            for td in tds:
                style = td.attrib.get("style")
                if style == "background-color: pink":
                    hasConstellation = True

            
            if hasConstellation: 
                star = processSingleStar(tds)
                systemsFormatted.append(star)
            else:
                star = processStarWithNineTds(tds)
                star['distance'] = distance
                star['stellarParallax'] = parallax
                index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
                systemsFormatted[index]['stars'].append(star)    
                
    
    return systemsFormatted

def processAllTrs(trs):
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
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
        if len(tds) == 6:
            star = processStarWithSixTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
            
        if len(tds) == 7:
            star = processStarWithSevenTds(tds)
            star['distance'] = distance
            star['constellation'] = constellation
            star['stellarParallax'] = parallax
            index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
            systemsFormatted[index]['stars'].append(star)
            
            
            
        if len(tds) == 9:
            hasConstellation = False

            for td in tds:
                style = td.attrib.get("style")
                if style == "background-color: pink":
                    hasConstellation = True

            
            if hasConstellation: 
                star = processSingleStar(tds)
                systemsFormatted.append(star)
            else:
                star = processStarWithNineTds(tds)
                star['distance'] = distance
                star['stellarParallax'] = parallax
                index = 0 if len(systemsFormatted) - 1 == -1 else len(systemsFormatted) - 1
                systemsFormatted[index]['stars'].append(star)    
                
    
    return systemsFormatted
    
def processSingleStar(tds): 
    systemObject = { "systemName": "N/A"  }
    starObject = {}
    starsArray = []
    for td in enumerate(tds):
        propertyKey, objectFormatted, images = formatStar(td, session)
        starObject['images'] = images or []
        starObject[propertyKey] = objectFormatted

    # If we didn't get images (e.g. colspan/rowspan row structure), try to find any useful link in the row.
    if not starObject.get('images'):
        for td in tds:
            hrefs = td.find_all('a')
            if not hrefs:
                continue
            href = hrefs[0].attrib.get('href')
            if not href or not href.startswith('/wiki/'):
                continue
            starObject['images'] = getImages('https://en.wikipedia.org' + href, session)
            if starObject['images']:
                break

    # Ensure systemName is populated even when the table doesn't explicitly include it
    if 'name' in starObject:
        systemObject['systemName'] = starObject['name']

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
            
    images = getImages("https://en.wikipedia.org" + hrefs[0].attrib["href"], session)
    
    starObject['images'] = images
    
    starsArray.append(starObject)
    systemObject["stars"] = starsArray
    return systemObject


def processStarWithFiveTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarFiveTds(td)
        starObject[propertyKey] = objectFormatted
            
    starObject['images'] = _fetch_images_from_row(tds)
    return starObject

def processStarWithSixTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarSixTds(td)
        starObject[propertyKey] = objectFormatted
            
    starObject['images'] = _fetch_images_from_row(tds)
    return starObject


def processStarWithSevenTds(tds):
    starObject = {}
    
    for td in enumerate(tds):
        propertyKey, objectFormatted = formatStarSevenTds(td)
        starObject[propertyKey] = objectFormatted
            
    starObject['images'] = _fetch_images_from_row(tds)
    return starObject

def processStarWithNineTds(tds):
    starObject = {}
    for td in enumerate(tds):

        propertyKey, objectFormatted = formatStarNineTds(td)
        starObject[propertyKey] = objectFormatted
            
    starObject['images'] = _fetch_images_from_row(tds)
    return starObject
