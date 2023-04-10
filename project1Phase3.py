# Name: Tyler Orme
# Date: 03/23/2023
# phase 1 of facility location project
# store the data into 4 seperate lists:
#  1. list of city names, cityList
#  2. list of city coordinates, coordList
#  3. list of city populations, popList
#  4. list of city distances, distanceList
#  *note: All lists have the same length, 128

# required functions:
# def loadData(cityList, coordList, popList, distanceList):
    # This function reads from the file miles.dat and loads information from this file into the
    # data structures cityList, coordList, popList, and distanceList. This function does
    # not return anything; it simply modifies these 4 lists in-place. The function assumes that
    # all 4 lists are empty before the function is called.
# def getCoordinates(cityList, coordList, name):
    # This function returns the list containing the latitude and longitude of the city name. You
    # can assume that name is a string of the form “cityName stateName” that appears in
    # cityList.
# def getPopulation(cityList, popList, name):
    # This function returns the population of the city name. You can assume that name is a
    # string of the form “cityName stateName” that appears in cityList.
# def getDistance(cityList, distanceList, name1, name2):
    # This function returns the distance between the two cities name1 and name2. You can
    # assume that name1 and name2 are strings of the form “cityName stateName” that appear
    # in cityList.
# def nearbyCities(cityList, distanceList, name, r):
    # This function returns the list of all cities with r miles of the city name. You can assume
    # that the city name name is a string of the form “cityname statename” that appears in
    # cityList. You can assume that r is a nonnegative floating point number. The list of cities
    # returned by your function should be in the same order as they appear in cityList.

###############################################################################
def loadData(cityList, coordList, popList, distanceList):

    #initalizing variable s to store distances
    s  = ''

    #open file
    file = open("miles.dat", "r")

    #skip first 4 lines
    for i in range(4):
        file.readline()
    
    #initalizing iterator to remember what line we are on
    i = 0

    #read in data
    for line in file:
        # reading city names, coordinates, and populations
        if ("A" <= line[0]) and (line[0] <= "Z"):
            # ADD CODE HERE to extract cityName and stateCode
            cityName = line[0:line.find(",")]
            stateCode = line[line.find(",")+2:line.find(",")+4]

            cityList.append(cityName + " " + stateCode)
            coordList.append([int(line[line.find("[")+1:line.find(',',line.find('['))]), int(line[line.find(',',line.find('['))+1:line.find(']')])])
            popList.append(int(line[line.find(']')+1:]))
            
            # avoids having 2 empty lists in list
            if i > 0:
                # print(s)
                L = s.split()
                # print(L)
                L.reverse()
                # print(L)
                distanceList.append(L)
                s = ''
            
        # reading distances
        elif ("0" <= line[0]) and (line[0] <= "9"):
            s = s + line

        # pick up the final list of distances
        elif line[0] == "*":
            if i > 0:
                # print(s)
                L = s.split()
                # print(L)
                L.reverse()
                # print(L)
                distanceList.append(L)
                s = ''

        #increase iterator   
        i += 1

    #convert list of strings into list of ints
    for i in range(len(distanceList)):
        for j in range(len(distanceList[i])):
            distanceList[i][j] = int(distanceList[i][j])
    
    #close file
    file.close()

    # print(distanceList)
    # print(cityList)
    # print(coordList)
    # print(popList)

###############################################################################


###############################################################################
def getCoordinates(cityList, coordList, name):
    return coordList[cityList.index(name)]
###############################################################################


###############################################################################
def getPopulation(cityList, popList, name):
    return popList[cityList.index(name)]
###############################################################################


###############################################################################
def getDistance(cityList, distanceList, name1, name2):
    if name1 == name2:
        return 0
    else:
        index1 = cityList.index(name1)
        index2 = cityList.index(name2)
        if index1 > index2:
            return distanceList[index1][index2]
        else:
            return distanceList[index2][index1]
###############################################################################


###############################################################################
def nearbyCities(cityList, distanceList, name, r):
    #return list of cities r length away from name city
    L = []
    cityPosition = cityList.index(name)
    # print(cityPosition)
    for i in range(len(cityList)):
        if i == cityPosition:
            for j in range(len(distanceList[i])):
                if distanceList[i][j] <= r:
                    L.append(cityList[j])
                else:
                    continue
        elif i > cityPosition and distanceList[i][cityPosition] <= r:
            L.append(cityList[i])

    return L
###############################################################################

#Test cases
# print(type(distanceList[1][0]))
# print(nearbyCities(cityList, distanceList, "Youngstown OH", 1000))
# print(getDistance(cityList, distanceList, "Youngstown OH", "Ravenna OH"))

#PHASE 2

# Greedy Algorithm for facility location
# 1. Initially all cities are unserved.
# 2. while there are cities that are unserved:
# 3. Pick a city c that “serves” the most unserved cities.
# 4. Mark the city c and all cities within r miles of c as served



###############################################################################
def locateFacilities(cityList, distanceList, r):

    # Initializing served cities
    served = [False] * len(cityList)

    # Nested function to find unserved cities
    def unservedCitiesAroundC(c, cityList, distanceList, r, served):
        # returns list of unserved cities within r miles of city C including the city C in order to be able to mark it as served
        unserved = []
        closeCities = nearbyCities(cityList, distanceList, c, r)
        
        for i in range(len(closeCities)):
            if served[cityList.index(closeCities[i])] == False:
                unserved.append(closeCities[i])
        return unserved
    # END FUNCTION

    # locate fewest number of facilities with coverage radius r to cover all cities
    facilities = []

    # while there are cities that are unserved:
    while False in served:

        # Pick a city c that “serves” the most unserved cities.
        maxUnserved = 0
        amountServed = []
        for i in range(len(cityList)):
            if served[i] == False:
                amountServed.append(len(unservedCitiesAroundC(cityList[i], cityList, distanceList, r, served))+1)
            elif served[i] == True:
                amountServed.append(len(unservedCitiesAroundC(cityList[i], cityList, distanceList, r, served)))

        c = cityList[amountServed.index(max(amountServed))]
        amountServed = []
            
        # Mark the city c and all cities within r miles of c as served
        facilities.append(c)
        served[cityList.index(c)] = True
        nowServedCities = nearbyCities(cityList, distanceList, c, r)
        for i in range(len(nowServedCities)):
            served[cityList.index(nowServedCities[i])] = True

    return facilities
###############################################################################

#Test cases
# print(locateFacilities(cityList, distanceList, 500))

#PHASE 3
# display the facilities onto google earth by creating KML file

###############################################################################
def fixCoords(coordList):
    # fixing coords by inserting decimal, leaving 2 decimal places (only works for northwest hemisphere)
      for i in range(len(coordList)):
        coordList[i][0] = float(str(coordList[i][0])[:-2]+ "." + str(coordList[i][0])[-2:])
        coordList[i][1] = float("-" + str(coordList[i][1])[:-2]+ "." + str(coordList[i][1])[-2:])
    # print(coordList)
###############################################################################


# ###############################################################################
def display(facilities, cityList, distanceList, coordList, r):
    # create kml file 
    kml = open("visualization{}.kml".format(r), "w")
    kml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n")
    kml.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\"> \n")
    kml.write("<Document>")
    kml.write("<name>visualization{}</name>".format(r))
    kml.write("<description>Visualization of facilities with range {}</description> \n".format(r))
  
    # styles for city points, facility pins, and lines
    kml.write("<Style id=\"city\"> \n")
    kml.write("<IconStyle> \n")
    kml.write("<Icon>  \n")
    kml.write("<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href> \n")
    kml.write("</Icon>  \n")
    kml.write("<scale>2</scale> \n")
    kml.write("</IconStyle> \n")
    kml.write("</Style> \n")

    kml.write("<Style id=\"facility\"> \n")
    kml.write("<IconStyle> \n")
    kml.write("<Icon>\n")
    kml.write("<href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>\n")
    kml.write("</Icon>\n")
    kml.write("<scale>2</scale>\n")
    kml.write("</IconStyle>\n")
    kml.write("</Style>\n")

    kml.write("<Style id=\"line\">\n")
    kml.write("<LineStyle>\n")
    kml.write("<color>ff0000ff</color>\n")
    kml.write("<width>2</width>\n")
    kml.write("</LineStyle>\n")
    kml.write("</Style>\n")

    # points for each city
    for i in range(len(cityList)):
        if cityList[i] in facilities:
            continue
        kml.write("<Placemark> \n")
        kml.write("<name>{}</name> \n".format(cityList[i]))
        kml.write("<styleUrl>#city</styleUrl> \n")
        kml.write("<Point> \n")
        kml.write("<coordinates>{}, {}</coordinates> \n".format(coordList[i][1], coordList[i][0]))
        kml.write("</Point> \n")
        kml.write("</Placemark> \n")

    # pins for each facility
    for i in range(len(facilities)):
        kml.write("<Placemark> \n")
        kml.write("<name>{}</name> \n".format(facilities[i]))
        kml.write("<styleUrl>#facility</styleUrl> \n")
        kml.write("<Point> \n")
        kml.write("<coordinates>{}, {}</coordinates> \n".format(coordList[cityList.index(facilities[i])][1], coordList[cityList.index(facilities[i])][0]))
        kml.write("</Point> \n")
        kml.write("</Placemark> \n")

    # line from cities not in facilities to nearest facility
    for i in range(len(cityList)):
        if cityList[i] not in facilities:
            nearestFacility = None  
            minDistance = 10000000  
            for j in range(len(facilities)):
                distance = getDistance(cityList, distanceList, cityList[i], facilities[j])
                if distance < minDistance:
                    minDistance = distance
                    nearestFacility = facilities[j]
            if nearestFacility != None:  
                kml.write("<Placemark> \n")
                kml.write("<name>{}</name> \n".format(cityList[i] + " to " + nearestFacility))
                kml.write("<styleUrl>#line</styleUrl> \n")
                kml.write("<LineString> \n")
                kml.write("<coordinates>{},{},0.0 {},{},0.0</coordinates> \n".format(coordList[cityList.index(cityList[i])][1], coordList[cityList.index(cityList[i])][0], coordList[cityList.index(nearestFacility)][1], coordList[cityList.index(nearestFacility)][0]))
                kml.write("</LineString> \n")
                kml.write("</Placemark> \n")

    # close kml file
    kml.write("</Document> \n")
    kml.write("</kml> \n")
    kml.close()
###############################################################################

# MAIN PROGRAM
###############################################################################
def main():

    #initalizing variables
    cityList = []
    coordList = []
    popList = []
    distanceList = []

    # load data
    loadData(cityList, coordList, popList, distanceList)

    # fixing coords
    fixCoords(coordList)

    # Output kml file with range 300
    r = 300
    facilities = locateFacilities(cityList, distanceList, r)
    print(facilities)
    display(facilities, cityList, distanceList, coordList, r) # creates kml file, visualization300.kml

    # Output kml file with range 800
    r = 800
    facilities = locateFacilities(cityList, distanceList, r)
    print(facilities)
    display(facilities, cityList, distanceList, coordList, r) # creates kml file, visualization800.kml


###############################################################################

#run program :)
main()

# fin