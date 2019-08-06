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


    # URL = "https://mslb1.longdo.com/map/mmroute-transit/json/route/raw?flon="+lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd
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
    checkerrorlist1 =[]
    checkerrorlist.append("latstart = "+str(latstart)+'\n')
    checkerrorlist.append("lonstart = "+str(lonstart)+'\n')
    checkerrorlist.append("latEnd = "+str(latEnd)+'\n')
    checkerrorlist.append("lonEnd = "+str(lonEnd)+'\n')    
    checkerrorlist.append("Node =  "+str(NodeStart)+","+str(NodeEnd)+'\n')
    c = False
    print(lonstart)
    print(latstart)
    print(lonEnd)
    print(latEnd)
    #-------------fromNode to ToNode-------------------------------------                         
    while count < len(datafromWWW):
        noterror = 0
        for datao in OurroadFinal2:
            if int(datafromWWW[count]['id']) == int(datao[1]):
                # linefinal.append(str(datao[1])+",P"+str(datao[2])+",P"+str(datao[3])+","+str(datafromWWW[count]['dir'])+'\n')
                FnodeCurrent = int(datao[2])
                TnodeCurrent = int(datao[3])
                # if FnodeCurrent == NodeStart or TnodeCurrent == NodeStart:
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
                if noterror != 1 and c: #กันการเปลี่ยน f node t nodeตรงกลาง #and len(Nodefinal) != 1 
                    linefinal2.append((datao[1],datao[2],datao[3])) #roadID Fnode Tnode
                    #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                    TnodeCurrent = int(datao[3])
                    sumlenn.append(float(datao[4]))
                    Nodefinal.append(datao[2])
                    testRoadIDwithQgis.append(
                    str(datafromWWW[count]['id'])+",")
                    noterror = 1
                if TnodeCurrent == NodeStart and c : #วนกลับมาจุดเดิม
                    num = 0
                    for dataa in linefinal2:
                        if int(datafromWWW[num]['id']) == int(dataa[0]):
                            datafromWWW.remove(datafromWWW[num])
                        else: 
                            num=num+1
                    linefinal2.clear()
                    Nodefinal.clear()
                    sumlenn.clear()
                    noterror = 1
                    c = False
                    count = -1 # มันจะบวกเพิ่มข้างล่าง
                break
        count = count+1
        b = 0

        if TnodeCurrent == NodeEnd or (FnodeCurrent == NodeEnd and len(Nodefinal)> 1):
            Nodefinal.append(TnodeCurrent)
            i = 0
            if len(linefinal2) == 0 and len(datafromWWW)!= 0:
                counterror.append("1")
                checkerrorlist1.append("linefinal ไม่มีข้อมูล")
                break
                # datafromWWW.remove(datafromWWW[0])
                # b = 1
                # count = 0
            while i < len(linefinal2)-1 :
                if linefinal2[i][2] !=  linefinal2[i+1][1] and linefinal2[i][2] !=  linefinal2[i+1][2] and linefinal2[i][1] !=  linefinal2[i+1][1] and linefinal2[i][1] !=  linefinal2[i+1][2]: #fnode Tnode ไม่ต่อกัน
                    count = 0
                    linefinal2.clear()
                    sumlenn.clear()
                    Nodefinal.clear()
                    counterror.clear()
                    checkerrorlist1.append(checkerrorlist2)
                    checkerrorlist2.clear()
                    testRoadIDwithQgis.clear()
                    c = False
                    datafromWWW.remove(datafromWWW[0]) #ลบตัวหน้า
                    b = 1
                i = i+1

            if b == 0 : #
                counterror.clear()
                checkerrorlist2.clear()
                break
            
        elif noterror != 1 and c:
            if len(Nodefinal) != 1:
                try:
                    linefinal2.clear()
                    sumlenn.clear()
                    Nodefinal.clear()
                    counterror.clear()
                    checkerrorlist2.clear()
                    testRoadIDwithQgis.clear()
                    c = False
                    checkerrorlist2.append(("ทำไมroadไอดี "+str(datafromWWW[count-1]['id'])+" ไม่มีในdatabase")+'\n')
                    counterror.append("1")
                except:
                    counterror.append("1")
                    checkerrorlist1.append("linefinal ไม่มีข้อมูล")
                # print("ไม่มีข้อมูลใน datafromWWW")
            # print(counterror)
    # for data in linefinal2:
    #     linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+'\n'))  
        # linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+str(datafromWWW[count]['dir'])+'\n'))

    #ย้อนกลับไปเป็นยังไม่ได้ทำไรเลย
    #-------------ToNode to FromNode----------------แค่สลับ--------------------- 
    a = NodeEnd
    b = NodeStart
    NodeStart = a
    NodeEnd = b
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
    # URL = "https://mslb1.longdo.com/map/mmroute-transit/json/route/raw?flon="+lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd
    CallData = requests.get(URL)
    # datafromWWW = [{'id': 554528, 'dir': 0}, {'id': 385389, 'dir': 1}]
    datafromWWW = CallData.json()  # ได้ข้อมูลทั้งหมดแล้ว
    count = 0
    sumlenn2 = []
    Nodefinal2 = []
    testRoadIDwithQgis2 = []
    linefinal3 = []
    counterror2 = []
    checkerrorlist3 = []
    checkerrorlist4 = []
    c = False
    while count < len(datafromWWW):
        noterror = 0
        for datao in OurroadFinal2:
            if int(datafromWWW[count]['id']) == int(datao[1]):
                # linefinal.append(str(datao[1])+",P"+str(datao[2])+",P"+str(datao[3])+","+str(datafromWWW[count]['dir'])+'\n')
                FnodeCurrent = int(datao[2])
                TnodeCurrent = int(datao[3])
                if FnodeCurrent == NodeStart :
                # if FnodeCurrent == NodeStart or TnodeCurrent == NodeStart : # บางครั้งจะมีแบบ ตัวแรกที่เข้ามาไม่ใช่จุดเริ่มต้นที่เราต้องการเข้ามาได้ไงก็ไม่รู้ก็สร้างifนี้ไว้เช็คเพื่อตัดการerrorเคสนั้นออก
                    c = True
                    # print(NodeStart)
                if c and str(FnodeCurrent) not in Nodefinal2:
                    linefinal3.append((datao[1],datao[2],datao[3]))
                    #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                    TnodeCurrent = int(datao[3])
                    sumlenn2.append(float(datao[4]))
                    Nodefinal2.append(datao[2])
                    testRoadIDwithQgis2.append(
                    str(datafromWWW[count]['id'])+",")
                    noterror = 1
                if noterror != 1 and c : #กันการเปลี่ยน f node t nodeตรงกลาง
                    linefinal3.append((datao[1],datao[2],datao[3])) #roadID Fnode Tnode
                    #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                    TnodeCurrent = int(datao[3])
                    sumlenn2.append(float(datao[4]))
                    Nodefinal2.append(datao[2])
                    testRoadIDwithQgis2.append(
                    str(datafromWWW[count]['id'])+",")
                    noterror = 1
                if TnodeCurrent == NodeStart and c:
                    num = 0
                    for dataa in linefinal3:
                        if int(datafromWWW[num]['id']) == int(dataa[0]):
                            datafromWWW.remove(datafromWWW[num])
                        else: 
                            num=num+1
                    linefinal3.clear()
                    Nodefinal2.clear()
                    sumlenn2.clear()
                    noterror = 1
                    c = False
                    count = -1 # มันจะบวกเพิ่มข้างล่าง
                break
        count = count+1
        b = 0
        if TnodeCurrent == NodeEnd or (FnodeCurrent == NodeEnd and len(Nodefinal)> 1):
            Nodefinal2.append(TnodeCurrent)
            i = 0
            if len(linefinal3) == 0 and len(datafromWWW)!= 0:
                counterror2.append("1")
                checkerrorlist3.append("linefinal ไม่มีข้อมูล")
                break
                # datafromWWW.remove(datafromWWW[0])
                # b = 1
                # count = 0
            while i < len(linefinal3)-1 : #เช็คว่าข้อมูลทั้งหมดต่อกันป่าว
                if linefinal3[i][2] !=  linefinal3[i+1][1] and linefinal3[i][2] !=  linefinal3[i+1][2] and linefinal3[i][1] !=  linefinal3[i+1][1] and linefinal3[i][1] !=  linefinal3[i+1][2]: #fnode Tnode ไม่ต่อกัน มีหลาย or เพราะสามารถกลับ t to f , f to t ได้
                    count = 0
                    linefinal3.clear()
                    sumlenn2.clear()
                    Nodefinal2.clear()
                    counterror2.clear()
                    checkerrorlist3.append(checkerrorlist4)
                    checkerrorlist4.clear()
                    testRoadIDwithQgis2.clear()
                    datafromWWW.remove(datafromWWW[0]) #ลบตัวหน้า
                    b = 1
                i = i+1

            if b == 0 : #
                counterror2.clear()
                checkerrorlist4.clear()
                break
            
        elif noterror != 1 and c:
            if len(Nodefinal2) != 1:
                try:
                    linefinal3.clear()
                    sumlenn2.clear()
                    Nodefinal2.clear()
                    counterror2.clear()
                    testRoadIDwithQgis2.clear()
                    c = False
                    checkerrorlist4.append(("ทำไมroadไอดี "+str(datafromWWW[count-1]['id'])+" ไม่มีในdatabase")+'\n')
                    counterror2.append("1")
                except:
                    linefinal3.clear()
                    sumlenn2.clear()
                    Nodefinal2.clear()
                    counterror2.clear()
                    testRoadIDwithQgis2.clear()
                    c = False
                    counterror2.append("1")
                    checkerrorlist3.append("linefinal ไม่มีข้อมูล")


    Nodefinal2.reverse()
    sumlenn2.reverse()
    linefinal3.reverse()
    if (sum(sumlenn2) < sum(sumlenn) and sum(sumlenn2)!=0)  or sum(sumlenn) == 0:
        sumlenn.clear()
        sumlenn.extend(sumlenn2)
        Nodefinal.clear()
        # Nodefinal.extend(Nodefinal2)
        testRoadIDwithQgis.clear()
        testRoadIDwithQgis.extend(testRoadIDwithQgis2)
        counterror.clear()
        counterror.extend(counterror2)
        checkerrorlist.extend(checkerrorlist3)
        for data in linefinal3 :
            linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+'\n'))
            if data[1] not in Nodefinal:
                Nodefinal.append(data[1])
            if data[2] not in Nodefinal:
                Nodefinal.append(data[2])
        # linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+str(datafromWWW[count]['dir'])+'\n'))
    elif (sum(sumlenn2) >= sum(sumlenn) and sum(sumlenn)!=0) or sum(sumlenn2) == 0 :
        checkerrorlist.extend(checkerrorlist1)
        Nodefinal.clear()
        for data in linefinal2 :
            linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+'\n'))  
            if data[1] not in Nodefinal:
                Nodefinal.append(data[1])
            if data[2] not in Nodefinal:
                Nodefinal.append(data[2])
        # linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+str(datafromWWW[count]['dir'])+'\n'))
    else:
        checkerrorlist.append("ไปไม่ได้สักทาง")
    #-------------ใช้อีก API-------------------------------------
    if len(counterror) > 0 : #แปลว่าข้างบน error
        for data in latlonNodelist:
            if NodeStart == int(data[2]):
                lonstart = str(data[0])
                latstart = str(data[1])
            if NodeEnd == int(data[2]):
                lonEnd = str(data[0])
                latEnd = str(data[1])

        URL = "https://mslb1.longdo.com/map/mmroute-transit/json/route/raw?flon="+lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd
        # URL = "https://mmmap15.longdo.com/mmroute/json/route/raw?flon=" + \
        #      lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd

        CallData = requests.get(URL)
        datafromWWW = CallData.json()  # ได้ข้อมูลทั้งหมดแล้ว
        count = 0
        Nodefinal12 = []
        testRoadIDwithQgis12 = []
        linefinal13 = []
        c = False
        while count < len(datafromWWW):
            noterror = 0
            for datao in OurroadFinal2:
                if int(datafromWWW[count]['id']) == int(datao[1]):
                    # linefinal.append(str(datao[1])+",P"+str(datao[2])+",P"+str(datao[3])+","+str(datafromWWW[count]['dir'])+'\n')
                    FnodeCurrent = int(datao[2])
                    TnodeCurrent = int(datao[3])
                    # if FnodeCurrent == NodeStart or TnodeCurrent == NodeStart:
                    if FnodeCurrent == NodeStart:  # บางครั้งจะมีแบบ ตัวแรกที่เข้ามาไม่ใช่จุดเริ่มต้นที่เราต้องการเข้ามาได้ไงก็ไม่รู้ก็สร้างifนี้ไว้เช็คเพื่อตัดการerrorเคสนั้นออก
                        c = True
                        # print(NodeStart)
                    if c and str(FnodeCurrent) not in Nodefinal12:
                        linefinal13.append((datao[1],datao[2],datao[3]))
                        #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                        TnodeCurrent = int(datao[3])
                        sumlenn.append(float(datao[4]))
                        Nodefinal12.append(datao[2])
                        testRoadIDwithQgis12.append(
                        str(datafromWWW[count]['id'])+",")
                        noterror = 1
                    if noterror != 1 and c: #กันการเปลี่ยน f node t nodeตรงกลาง #and len(Nodefinal) != 1 
                        linefinal13.append((datao[1],datao[2],datao[3])) #roadID Fnode Tnode
                        #linefinal2.append((datao[1],datao[2],datao[3],datafromWWW[count]['dir']))
                        TnodeCurrent = int(datao[3])
                        sumlenn.append(float(datao[4]))
                        Nodefinal12.append(datao[2])
                        testRoadIDwithQgis12.append(
                        str(datafromWWW[count]['id'])+",")
                        noterror = 1
                    if TnodeCurrent == NodeStart and c : #วนกลับมาจุดเดิม
                        num = 0
                        for dataa in linefinal13:
                            if int(datafromWWW[num]['id']) == int(dataa[0]):
                                datafromWWW.remove(datafromWWW[num])
                            else: 
                                num=num+1
                        linefinal13.clear()
                        Nodefinal12.clear()
                        sumlenn.clear()
                        noterror = 1
                        c = False
                        count = -1 # มันจะบวกเพิ่มข้างล่าง
                    break
            count = count+1
            b = 0

            if TnodeCurrent == NodeEnd or (FnodeCurrent == NodeEnd and len(Nodefinal)> 1):
                Nodefinal12.append(TnodeCurrent)
                i = 0
                if len(linefinal13) == 0 and len(datafromWWW)!= 0:
                    counterror.append("1")
                    checkerrorlist1.append("linefinal ไม่มีข้อมูล")
                    break
                    # datafromWWW.remove(datafromWWW[0])
                    # b = 1
                    # count = 0
                print(linefinal13)
                while i < len(linefinal13)-1 :
                    if linefinal13[i][2] !=  linefinal13[i+1][1] and linefinal13[i][2] !=  linefinal13[i+1][2] and linefinal13[i][1] !=  linefinal13[i+1][1] and linefinal13[i][1] !=  linefinal13[i+1][2]: #fnode Tnode ไม่ต่อกัน
                        count = 0
                        linefinal13.clear()
                        sumlenn.clear()
                        Nodefinal12.clear()
                        counterror.clear()
                        checkerrorlist1.append(checkerrorlist2)
                        checkerrorlist2.clear()
                        testRoadIDwithQgis12.clear()
                        c = False
                        datafromWWW.remove(datafromWWW[0]) #ลบตัวหน้า
                        b = 1
                    print(i)    
                    i = i+1
                    

                if b == 0 : #
                    counterror.clear()
                    checkerrorlist2.clear()
                    break
                
            elif noterror != 1 and c:
                if len(Nodefinal12) != 1:
                    try:
                        linefinal13.clear()
                        sumlenn12.clear()
                        Nodefinal12.clear()
                        counterror.clear()
                        checkerrorlist2.clear()
                        testRoadIDwithQgis12.clear()
                        c = False
                        checkerrorlist2.append(("ทำไมroadไอดี "+str(datafromWWW[count-1]['id'])+" ไม่มีในdatabase")+'\n')
                        counterror.append("1")
                    except:
                        counterror.append("1")
                        checkerrorlist1.append("linefinal ไม่มีข้อมูล")
        checkerrorlist.extend(checkerrorlist2)
        Nodefinal.clear()
        for data in linefinal13 :
            linefinal.append(str(data[0]+",P"+str(data[1])+",P"+str(data[2])+'\n'))  
            if data[1] not in Nodefinal:
                Nodefinal.append(data[1])
            if data[2] not in Nodefinal:
                Nodefinal.append(data[2])



        
 











    








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
    sumlongfoeline = []
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
    sumlongfoeline = []
    sumlongforpoint = []
    testnew = []
    a = ''
    b = ''
    c = ''
    d = ''
    e = ''
    f1 = 0
    f2 = 0
    last1  = 0
    last2 = 0
    ii = 0
    jj = 0
    for datacut in linefinal:
        datacut = datacut.strip('\n')
        datacut = datacut.split(',')
        sumlongfoeline.append(datacut)
    for datap in Pointfinal:
        datap = datap.strip('\n')
        datap = datap.split(',')
        sumlongforpoint.append(datap)
    while ii < len(sumlongfoeline): #ตัดตัวซ้ำที่ติดกัน
        if (ii+1) == len(sumlongfoeline):
            break
        if sumlongfoeline[ii] == sumlongfoeline[ii+1]:
            sumlongfoeline.remove(sumlongfoeline[ii+1])
        ii = ii +1
    while jj < len(sumlongforpoint):
        if (jj+1) == len(sumlongforpoint):
            break
        if sumlongforpoint[jj] == sumlongforpoint[jj+1]:
            sumlongforpoint.remove(sumlongforpoint[jj+1])
        jj = jj +1

    
    j = 0 
    a1 = 0

    while j < len(sumlongfoeline):
        ab = True 
        aa = True
        i = 0
        while  i < len(sumlongforpoint):
            if len(sumlongfoeline) == len(testnew):
                break
            if str(sumlongfoeline[j][1]) == str(sumlongforpoint[i][0]) and ab :
                ab = False
                a =  str(sumlongfoeline[j][0]) #roadid
                b = str(sumlongforpoint[i][1]) #x y

                try : 
                    if sumlongforpoint[i][0] == sumlongfoeline[j+1][1] or sumlongforpoint[i][0] == sumlongfoeline[j+1][2] :
                        i = -1
                        
                    else:
                        sumlongforpoint.remove(sumlongforpoint[i])
                except:
                    last1 = 1
                i = -1
            if str(sumlongfoeline[j][2]) == str(sumlongforpoint[i][0]) and aa:
                aa = False
                d = str(sumlongforpoint[i][1])#x y 
                f2 = f2+1
                try :
                    if sumlongforpoint[i][0] == sumlongfoeline[j+1][1] or sumlongforpoint[i][0] == sumlongfoeline[j+1][2] :
                        i = -1
                        
                    else:
                        sumlongforpoint.remove(sumlongforpoint[i])
                except:
                    last2 = 1
                i = -1
            if aa == False and ab == False:
                break
            else:
                i = i +1

            # elif aa == False or ab == False:
            #     i = i+1
            #     continue
            # elif aa and ab:
            #     i = i+1
        if aa or ab:
            a1 =a1+1
            print('error')

            
            if aa :
                print(str(sumlongfoeline[j][2]))
            if ab:
                print(str(sumlongfoeline[j][1]))
        else:
            testnew.append(a+",P"+b+",P"+d+'\n')
        j = j+1
    print(a1)

            

    file = open('P_Boss.txt', 'w')
    writetxt(file, testnew)

            






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
