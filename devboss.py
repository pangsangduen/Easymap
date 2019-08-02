# This Python file uses the following encoding: utf-8
import os
import psycopg2
import math
import requests
AllroadId = []

def main():
    nodeline = []
    count = 1
    with open("dataxy.txt" , 'r') as file:
        for line in file:
            if(count == 3):
                count = 1
                continue
            count = count + 1
            nodeline.append(line.strip())
    nodeFrom , nodeTo = splitLineTodata(nodeline)
    # getLatLon(nodeFrom , nodeTo)
    dic = nodeXY(nodeline)
    WriteFromTo(nodeFrom , nodeTo, dic)
    WriteXY(nodeline , dic)
    # WriteFromToXY(dic)

def WriteFromTo(nodeFrom , nodeTo , dic):
    # print(nodeFrom)
    index  = 0 
    with open("finalline.txt" , 'w') as file:
        for nf , nt in zip( nodeFrom , nodeTo):
        # print(dic[nf]["X"])
            nfX = dic[nf]["X"]
            nfY = dic[nf]["Y"]
            ntX = dic[nt]["X"]
            ntY = dic[nt]["Y"]
            file.write(str(index)+",P"+str(nfX)+" "+str(nfY)+",P"+str(ntX)+" "+str(ntY)+"\n")
            index = index +1 
    file.close()
    print("Write From To => finalline.txt")



def WriteXY(node , dic):
    with open("finalPoint.txt" , 'w') as file:
        for data in node:
            X = dic[data.split(" ")[0]]["X"].replace(".", "")
            Y = dic[data.split(" ")[0]]["Y"].replace(".", "")
            file.write("P"+str(X)+" "+str(Y)+","+str(data.split(" ")[1])+" "+str(data.split(" ")[2])+"\n")
    file.close()
    print("Write From To => finalPoint.txt")


def nodeXY(nodeline):
    XYdic = dict()
    for data in nodeline:
        XYdic[data.split(" ")[0]] = { "X" : data.split(" ")[1] , "Y" : data.split(" ")[2]}
    return (XYdic)

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
    return (nodeFrom,  nodeTo)

def getLatLon(nodeFrom , nodeTo):
    latlonObj = dict()
    with open("latlonFinishNodelist.txt" , 'r') as file:
        for line in file:
            nodeId = (line.split(",")[2].strip())
            latlonObj[nodeId] = {"lon" : line.split(",")[0] , "lat" : line.split(",")[1]}

    # for nf,nt in zip( nodeFrom , nodeTo):
    #     URL = "https://mmmap15.longdo.com/mmroute/json/route/raw?flon=" + latlonObj[nf]["lon"]+"&flat="+latlonObj[nf]["lat"]+"&tlon="+latlonObj[nt]["lon"]+"&tlat="+latlonObj[nt]["lat"]
    #     response = requests.get(URL).json()
    #     print(response)
    #     for result in response:
    #         AllroadId.append(result["id"])
    # outputfile = 'devboss.txt'
    # file = open(outputfile, 'w')
    # for data in AllroadId:
    #     file.write(str(data)+",")
    # file.close()
    # print("Done Write File => "+outputfile)


if __name__ == "__main__":
    main()