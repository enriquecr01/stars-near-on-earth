def formatStar(tdNumber):
    if tdNumber[0] == 0:
        return "name", tdNumber[1].text
    if tdNumber[0] == 1:
        return "distance", tdNumber[1].text
    if tdNumber[0] == 2:
        return "constelation", tdNumber[1].text
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
    if tdNumber[0] == 9:
        return "notes", tdNumber[1].text
    return "none", 0