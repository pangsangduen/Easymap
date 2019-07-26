# This Python file uses the following encoding: utf-8
import os
import psycopg2
import math
import requests

def main():
    nodeline = []
    count = 1
    with open("FinalXY.txt" , 'r') as file:
        for line in file:
            if(count == 3):
                count = 1
                continue
            count = count + 1
            nodeline.append(line.strip())
    splitLineTodata(nodeline)


def splitLineTodata(allline):
    nodeFrom = []
    nodeTo = []
    index = 0
    for node in allline:
        if index % 2 == 0 :
            nodeFrom.append(node.split()[0])
        else:
            nodeTo.append(node.split()[0])
        index = index +1
    getLatLon(nodeFrom,  nodeTo)

def getLatLon(nodeFrom , nodeTo):
    latlonObj = dict()
    AllroadId = []
    with open("latlonFinishNodelist.txt" , 'r') as file:
        for line in file:
            nodeId = (line.split(",")[2].strip())
            latlonObj[nodeId] = {"lon" : line.split(",")[0] , "lat" : line.split(",")[1]}

    for nf,nt in zip( nodeFrom , nodeTo):
        # print(latlonObj[nf]["lon"])
        URL = "https://mmmap15.longdo.com/mmroute/json/route/raw?flon=" + latlonObj[nf]["lon"]+"&flat="+latlonObj[nf]["lat"]+"&tlon="+latlonObj[nt]["lon"]+"&tlat="+latlonObj[nt]["lat"]
        response = requests.get(URL).json()
        print(response)
        for result in response:
            AllroadId.append(result["id"])
    outputfile = 'devboss.txt'
    file = open(outputfile, 'w')
    for data in AllroadId:
        file.write(str(data)+",")
    file.close()
    print("Done Write File => "+outputfile)


if __name__ == "__main__":
    main()



