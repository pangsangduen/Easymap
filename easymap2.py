import os  # เพราะเป็น os
import psycopg2
import math
import requests


def sql(result, nameroadlist):
    con = psycopg2.connect(database='turntable20190613', user='trainee',
                           password='mm2019', host='192.168.1.151', port='5433')
    cur = con.cursor()
    # cur.execute("SELECT r_name_t,gid,f_node,t_node FROM road where r_char < 6 ")
    cur.execute(
        "SELECT r_name_t,road_id,f_node,t_node,length FROM road where r_char < 7 ")
    result = cur.fetchall()
    cur.close()
    # print(result)
    # print(len(result))
    SqlToList(nameroadlist, result)


def SqlToList(nameroadlist, result):
    i = 0
    while len(nameroadlist) < len(result):
        a = result[i]
        # print(a)
        i = i+1
        nameroadlist.append(a)


# ดูว่าชื่อถนนในtxtของเราตัวไหนตรงกับในdatabase แต่ตอนนี้ตรงทุกตัวแล้ว
def ReadtxtToList(filepath, datafromsheet, nameroadlist, ourroad):
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            road = line.strip()
            Ourroad(road, nameroadlist, ourroad)
        #    print(road)
            datafromsheet.append(road)
            line = fp.readline()
            cnt += 1
        # print(datafromsheet)


def Ourroad(road, nameroadlist, ourroad):
    j = 0
    while j < len(nameroadlist)-1:
        j = j+1
        if nameroadlist[j][0].endswith(road):
            ourroad.append(nameroadlist[j])
    # print(ourroad)

# def  CutMap(ourroad,taaa203,gidlist,roadlist,lengthlist):
#     index = 0
#     numGid = 0
#     while index < len(ourroad):
#         road = ourroad[index][0]
#         Gid = ourroad[index][1]
#         lengthh = ourroad[index][4]
#         roadlist.append(road+"\n")
#         if road not in taaa203:
#             numGid = 0
#             taaa203.append(road)

#         if road in taaa203:
#             numGid = numGid+1
#             gidlist.append(str(Gid)+",")
#             lengthlist.append(str(lengthh)+"\n")
#         index+= 1
#     gidlist.append(numGid)
#     #print(gidlist)
#     print("ชื่อเส้นถนนที่หาเจอทั้งหมด  ="+str(len(taaa203)))


# def GidAll(ourroad):
#     ourGid = []
#     index = 0
#     while index < len(ourroad):
#         Gid = ourroad[index][1]
#         if Gid not in ourGid:
#             ourGid.append(Gid)
#         index+=1
#     #print(ourGid)
#     print("เราต้องทำ x y ทั้งหมด  ="+str(len(ourGid)))

def createXY(checkerrorlist,counterror,lonstart,latstart,Xstart,lonEnd,latEnd, Ystart, Xend, Yend, sumlenn, Nodefinal, Pointfinal):  # หาค่า xy สับๆ
    try:
        reseultX = Xstart  # จะเลื่อนไปเรื่อยๆจนถึง Xend
        reseultY = Ystart
        sumLength = sum(sumlenn)
        # Pointfinal.append("P"+str(Nodefinal[0])+","+str(reseultX)+" "+str(reseultY)+'\n')
        Pointfinal.append(
            "P"+str(Nodefinal[0])+","+str(reseultX)+" "+str(reseultY)+","+"2"+'\n')
        b = 1 
        for data in sumlenn:
            if abs(Ystart-Yend) == 0:  # แนวตั้ง
                # หาเปอเซนเทียบกับระยะห่าง xy แล้ว
                persentX = (data * (Xend-Xstart)) / sumLength
                reseultX = reseultX + persentX  # ได้ค่า xy ตัวใหม่ สับๆ
                # Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(Yend)+'\n')
                Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(Yend)+","+"2"+'\n')
                b = b+1
                if reseultX == Xend:
                    break
            elif abs(Xstart-Xend) == 0:  # แนวนอน
                persentY = (data * (Yend-Ystart)) / sumLength
                reseultY = reseultY + persentY  # ได้ค่า xy ตัวใหม่ สับๆ
                # Pointfinal.append("P"+str(Nodefinal[b])+","+str(Xend)+" "+str(reseultY)+'\n')
                Pointfinal.append("P"+str(Nodefinal[b])+","+str(Xend)+" "+str(reseultY)+","+"2"+'\n')
                b = b+1
                if reseultY == Yend:
                    break
            else:  # แนวเฉียง
                persentX = (data * (Xend-Xstart)) / sumLength
                persentY = (data * (Yend-Ystart)) / sumLength
                reseultX = reseultX + persentX  # ได้ค่า xy ตัวใหม่ สับๆ
                reseultY = reseultY + persentY  # ได้ค่า xy ตัวใหม่ สับๆ
                # Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(reseultY)+'\n')
                Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(reseultY)+","+"2"+'\n')
                b = b+1
        if reseultY != Yend or reseultX != Xend:
            # print(len(Pointfinal))
            # print(b)
            # Pointfinal[len(Pointfinal)-1]=("P"+str(Nodefinal[b-1])+","+str(Xend)+" "+str(Yend)+'\n')
            Pointfinal[len(Pointfinal)-1] = ("P"+str(Nodefinal[b-1])+","+str(Xend)+" "+str(Yend)+","+"2"+'\n')
    except:
        print(lonstart)
        print(latstart)
        print(lonEnd)
        print(latEnd)
        counterror.append("1")
        checkerrorlist.append("Nodefinal ไม่มีข้อมูล")
# เหลือเอาเข้าทั้งหมดแบบtxt


def prangNode(test, filepath):
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            road = line.strip()
            test.append(str(road))
            line = fp.readline()
            cnt += 1
        # print(test)


def createOurFnodeTnode(nameroadlist, roadIDlist, roadlist, lengthlist, Fnode, Tnode, test, ourroad, OurroadFinal, FTnode, OurroadFinal1):
    a = 0
    while a < len(ourroad):
        # print(nameroadlist[a][2])
        if str(ourroad[a][2]) in test and str(ourroad[a][3]) in test:
            #print (a)
            # roadIDlist.append(str(ourroad[a][1])+'\n')
            # roadlist.append(str(ourroad[a][0])+'\n')
            # lengthlist.append(str(ourroad[a][4])+'\n')
            Fnode.append(str(ourroad[a][2])+',')
            Tnode.append(str(ourroad[a][3])+',')
            # FTnode.append((ourroad[a][2],ourroad[a][3]))
            OurroadFinal.append(
                (ourroad[a][0], ourroad[a][1], ourroad[a][2], ourroad[a][3], ourroad[a][4]))
            OurroadFinal1.append(str(ourroad[a][0])+","+str(ourroad[a][1])+","+str(
                ourroad[a][2])+","+str(ourroad[a][3])+","+str(ourroad[a][4])+'\n')
        a = a+1
    # print(OurroadFinal[0][0])


# def SortNode(OurroadFinal2,OurroadSort1,nameRoad,nameRoadSame,NodeStart,NodeEnd,sumlenn,linefinal,Nodefinal):
#     check = 0
#     a = 0
#     count = 0
#     for data in OurroadFinal2:
#         if data[0] in  nameRoad:
#             nameRoadSame.append(data) #เอาชื่อถนนที่เหมือน
#     print(nameRoadSame)

#     for data in nameRoadSame: #ใส่ตัวแรก
#         #print(data[2])
#         if int(data[2]) == NodeStart:
#             print("aaaaaaa")
#             OurroadSort1.append(data) #ใส่ data ตัวแรก
#             sumlenn.append(float(data[4]))
#             linefinal.append(str(data[1])+',P'+str(data[2])+',P'+str(data[3])+'\n')
#             Nodefinal.append(str(data[2]))

#     if int(OurroadSort1[a][3]) == NodeEnd:  # ถ้ามีแค่roadIDเดียว
#         check = 1
#         count = len(nameRoadSame)
#     while count < len(nameRoadSame):
#         print(a)
#         for data in nameRoadSame:
#             if OurroadSort1[a][3] == data[2] :
#                 OurroadSort1.append(data)
#                 sumlenn.append(float(data[4]))
#                 Nodefinal.append(str(data[2]))
#                 linefinal.append(str(data[1])+',P'+str(data[2])+',P'+str(data[3])+'\n')
#                 #print(data[4])
#                 a=a+1
#                 break
#         count +=1

#         if int(OurroadSort1[a][3]) == NodeEnd:
#             check = 1
#             break
#     Nodefinal.append(NodeEnd)
#     print(Nodefinal)
#     if check != 1:
#          print("error จบไม่ตรง")

def MatchTxtWithLatlon(lonstart,latstart,lonEnd,latEnd,listtt, checkerrorlist, counterror, testRoadIDwithQgis, linefinal, Nodefinal, sumlenn, NodeStart, Xstart, Ystart, NodeEnd, Xend, Yend, latlonNodelist, listFromFinalStart, listFromFinalEnd, OurroadFinal2):

    for data in latlonNodelist:
        if NodeStart == int(data[2]):
            lonstart = str(data[0])
            latstart = str(data[1])
            # listFromFinalStart.append(data[0]) # ได้ lonstart = listFromFinalStart[0]
            # listFromFinalStart.append(data[1]) # latstart = listFromFinalStart[1]
        if NodeEnd == int(data[2]):
            lonEnd = str(data[0])
            latEnd = str(data[1])
            # listFromFinalEnd.append(data[0]) # ได้ lonEnd = listFromFinalEnd[0]
            # listFromFinalEnd.append(data[1]) # ได้ latEnd = listFromFinalEnd[1]

    URL = "https://mmmap15.longdo.com/mmroute/json/route/raw?flon=" + \
        lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd
    CallData = requests.get(URL)
    # datafromWWW = [{'id': 554528, 'dir': 0}, {'id': 385389, 'dir': 1}]
    datafromWWW = CallData.json()  # ได้ข้อมูลทั้งหมดแล้ว
    # print(len(datafromWWW))
    count = 0
    TnodeCurrent = 0
    FnodeCurrent = 0
    check = 0
    linefinal2 = []
    checkerrorlist2 =[]
    c = False
    print(lonstart)
    print(latstart)
    print(lonEnd)
    print(latEnd)
    checkerrorlist.append("lonstart = "+str(lonstart)+'\n')
    checkerrorlist.append("latstart = "+str(latstart)+'\n')
    checkerrorlist.append("lonEnd = "+str(lonEnd)+'\n')
    checkerrorlist.append("latEnd = "+str(latEnd)+'\n')
    checkerrorlist.append("NodeStart,NodeEnd = " +
                          str(NodeStart)+','+str(NodeEnd)+'\n')
    while count < len(datafromWWW):
        noterror = 0
        for datao in OurroadFinal2:
            if int(datafromWWW[count]['id']) == int(datao[1]):
                # linefinal.append(str(datao[1])+",P"+str(datao[2])+",P"+str(datao[3])+","+str(datafromWWW[count]['dir'])+'\n')
                FnodeCurrent = int(datao[2])
                if FnodeCurrent == NodeStart:  # บางครั้งจะมีแบบ ตัวแรกที่เข้ามาไม่ใช่จุดเริ่มต้นที่เราต้องการเข้ามาได้ไงก็ไม่รู้ก็สร้างifนี้ไว้เช็คเพื่อตัดการerrorเคสนั้นออก
                    c = True
                    # print(NodeStart)
                if c and str(FnodeCurrent) not in Nodefinal:
                    linefinal2.append((datao[1],datao[2],datao[3]))
                    #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                    TnodeCurrent = int(datao[3])
                    sumlenn.append(float(datao[4]))
                    Nodefinal.append(datao[2])
                    testRoadIDwithQgis.append(
                    str(datafromWWW[count]['id'])+",")
                    noterror = 1
                if noterror != 1 and len(Nodefinal) != 1: #กันการเปลี่ยน f node t nodeตรงกลาง
                    linefinal2.append((datao[1],datao[2],datao[3])) #roadID Fnode Tnode
                    #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                    TnodeCurrent = int(datao[3])
                    sumlenn.append(float(datao[4]))
                    Nodefinal.append(datao[2])
                    testRoadIDwithQgis.append(
                    str(datafromWWW[count]['id'])+",")
                    noterror = 1

                break
        count = count+1
        b = 0
        if TnodeCurrent == NodeEnd:
            Nodefinal.append(TnodeCurrent)
            i = 0
            if len(linefinal2) == 0:
                counterror.append("1")
                checkerrorlist.append("linefinal ไม่มีข้อมูล")
                break
            while i < len(linefinal2)-1 :
                if linefinal2[i][2] !=  linefinal2[i+1][1]: #fnode Tnode ไม่ต่อกัน
                    count = 0
                    linefinal2.clear()
                    sumlenn.clear()
                    Nodefinal.clear()
                    counterror.clear()
                    checkerrorlist2.clear()
                    datafromWWW.remove(datafromWWW[0]) #ลบตัวหน้า
                    b = 1
                i = i+1
            
                

            for data in linefinal2:
                linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+'\n'))  
                # linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+str(datafromWWW[count]['dir'])+'\n'))

            if b == 0 :
                checkerrorlist.append(checkerrorlist2)
                break

        elif noterror != 1 and c:
            try:
                checkerrorlist2.append(("ทำไมroadไอดี "+str(datafromWWW[count-1]['id'])+" ไม่มีในdatabase")+'\n')
                counterror.append("1")
            except:
                counterror.append("1")
                checkerrorlist.append("linefinal ไม่มีข้อมูล")
                # print("ไม่มีข้อมูลใน datafromWWW")
            # print(counterror)




def writetxt(file, ourroad):
    for data in ourroad:
        data = str(data)
        file.write(data)
    file.close()


def main():
    Pointfinal = []
    linefinal = []
    checkerrorlist = []
    OurroadFinal2 = []
    testRoadIDwithQgis = []
    listtt = []
    lonstart = ""
    latstart = " "
    lonEnd = " "
    latEnd = " "
    # filepath = 'nameroad1.txt'
    # file = open('testfile.txt','w')
    # sql(result,nameroadlist)
    # ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad)
    # CutMap(ourroad,taaa203,gidlist,roadlist,lengthlist)
    # writetxt(file,ourroad)
    # GidAll(ourroad)
    # file = open('roadlist.txt','w')
    # writetxt(file,roadlist)
    # file = open('gidlist.txt','w')
    # writetxt(file,gidlist)
    # file = open('lengthlist.txt','w')
    # writetxt(file,lengthlist)
    # file = open('testplot.txt','w')
    # i=0
    # while i < len(ourroad) :
    #     data = str(ourroad[i][2])+','+str(ourroad[i][3])+ ','
    #     data = str(data)
    #     file.write(data)
    #     i+=1
    # filepath = 'node.txt'         #  แปลงโหนดจากเว้นบรรทัดเป็น ,
    # prangNode(test,filepath)
    # file = open('node2.txt','w')
    # writetxt(file,str(test)+",")
    # createOurFnodeTnode(nameroadlist,roadIDlist,roadlist,lengthlist,Fnode,Tnode,test,ourroad,OurroadFinal,FTnode,OurroadFinal1)
    # file = open('roadlist.txt','w')
    # writetxt(file,roadlist)
    # file = open('roadIDlist.txt','w')
    # writetxt(file,roadIDlist)
    # file = open('Tnodelist.txt','w')
    # writetxt(file,Tnode)
    # file = open('Fnodelist.txt','w')
    # writetxt(file,Fnode)
    # file = open('lengthlist.txt','w')
    # writetxt(file,lengthlist)
    # filepath = 'node.txt'
    # with open(filepath) as fp:
    #     line = fp.readline()
    #     cnt = 1
    #     while line:
    #         road=line.strip()
    #         test.append(str(road))
    #         line = fp.readline()
    #         cnt += 1
    # print(test)
# เปลี่ยน
# -------------------------------------------------------------------
    filepath = 'OurroadFinal.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = line.strip()
            line = line.split(",")
            OurroadFinal2.append((line[0], line[1], line[2], line[3], line[4]))
            line = fp.readline()
    # print(OurroadFinal2)

    latlonNodelist = []
    filepath = 'latlonFinishNodelist.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            # count = count +1
            # print(count)
            line = line.strip()
            line = line.split(',')
            latlonNodelist.append((line[0], line[1], line[2]))
            line = fp.readline()
    # print(latlonNodelist[1])

    countLineFromFinalXY = 0
    counterror = []
    counterrorr = 0

    # nameRoadSame = []
    # nameRoad = []
    filepath = 'FinalXY.txt'
    with open(filepath) as fp:
        line = fp.readline()  # บรรทัดแรก
        while line:
            listFromFinalEnd = []
            listFromFinalStart = []
            line = line.strip()
            line = line.split(" ")
            NodeStart = int(line[0])
            Xstart = float(line[1])
            Ystart = float(line[2])
            line = fp.readline()
            line = line.split(" ")
            NodeEnd = int(line[0])
            Xend = float(line[1])
            Yend = float(line[2])
            line = fp.readline()  # อ่านบรรทัดที่ 3 แบบทิ้งๆไป
            sumlenn = []
            Nodefinal = []
            MatchTxtWithLatlon(lonstart,latstart,lonEnd,latEnd,listtt, checkerrorlist, counterror, testRoadIDwithQgis, linefinal, Nodefinal, sumlenn, NodeStart, Xstart, Ystart, NodeEnd, Xend, Yend, latlonNodelist, listFromFinalStart, listFromFinalEnd, OurroadFinal2)
            createXY(checkerrorlist,counterror,lonstart,latstart,Xstart,lonEnd,latEnd, Ystart, Xend, Yend, sumlenn, Nodefinal, Pointfinal)  # หาค่า xy สับๆ

            countLineFromFinalXY = countLineFromFinalXY + 3
            if len(counterror) > 0:
                counterrorr = counterrorr + 1
                checkerrorlist.append("errorข้างบน")
            counterror = []
            print("จากทั้งหมด "+str(countLineFromFinalXY / 3) +
                  " คู่ มีerrorทั้งหมด "+str(counterrorr)+" คู่")
            print("ถึงบรรทัดที่ "+str(countLineFromFinalXY))
            checkerrorlist.append('\n')
            line = fp.readline()

    file = open('finalLine.txt', 'w')
    writetxt(file, linefinal)
    file = open('finalPoint.txt', 'w')
    writetxt(file, Pointfinal)
    file = open('testRoadIDwithQgis.txt', 'w')
    writetxt(file, testRoadIDwithQgis)
    file = open('checkerrorlist.txt', 'w')
    writetxt(file, checkerrorlist)

    # print(listtt)
    # ---------------------------------------------------------
    # file = open('roadSort.txt','w')
    # writetxt(file,roadSort)
    # file = open('roadIDSort.txt','w')
    # writetxt(file,roadIDSort)
    # file = open('fnodeSort.txt','w')
    # writetxt(file,fnodeSort)
    # file = open('tnodeSort.txt','w')
    # writetxt(file,tnodeSort)
    # file = open('lenSort.txt','w')
    # writetxt(file,lenSort)
    # file = open('XYlist.txt','w')
    # writetxt(file,XYlist)
    # file = open('OurroadFinal.txt','w')
    # writetxt(file,OurroadFinal1)
    # ----------------------------------------------------------
    # latlonNodelist =[]
    # filepath = 'latlonFromNode.txt'
    # # count =0
    # with open(filepath) as fp:
    #     line = fp.readline()
    #     while line:
    #         # count = count +1
    #         # print(count)
    #         line = line.strip("Point").strip()
    #         line=line.strip("(").strip()
    #         line = line.split(' ')
    #         latitem = line[1].split(')\t')[0]
    #         nodeitem = line[1].split(')\t')[1]
    #         latlonNodelist.append((str(line[0])+","+str(latitem)+","+str(nodeitem)+'\n'))
    #         line = fp.readline()
    # file = open('latlonFinishNodelist.txt','w')
    # writetxt(file,latlonNodelist)
    # ------^^--แปลง txt Point (100.7110034185211731 13.99387910510712807)	1197198 เป็น lat,lon,point


if __name__ == "__main__":
    main()
