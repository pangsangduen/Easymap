# แก้ node.txt เพิ่มชื่อถนน
import os # เพราะเป็น os
import psycopg2
import math
import requests

def sql(result,nameroadlist):
    con = psycopg2.connect(database = 'turntable20190613',user = 'trainee', password = 'mm2019', host = '192.168.1.151', port = '5433')
    cur = con.cursor()
    # cur.execute("SELECT r_name_t,gid,f_node,t_node FROM road where r_char < 6 ")
    cur.execute("SELECT r_name_t,road_id,f_node,t_node,length FROM road where r_char < 7 ")
    result = cur.fetchall()
    cur.close()
    # print(result)
    #print(len(result))
    SqlToList(nameroadlist,result)

def SqlToList(nameroadlist,result):
    i = 0
    while len(nameroadlist) < len(result):
        a = result[i]
        # print(a)
        i =i+1
        nameroadlist.append(a)

def ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad): # ดูว่าชื่อถนนในtxtของเราตัวไหนตรงกับในdatabase แต่ตอนนี้ตรงทุกตัวแล้ว
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 1
        while line:
            road=line.strip()
            Ourroad(road,nameroadlist,ourroad)
        #    print(road)
            datafromsheet.append(road)
            line = fp.readline()
            cnt += 1
        #print(datafromsheet)

def Ourroad(road,nameroadlist,ourroad):
    j = 0
    while j < len(nameroadlist)-1:
        j=j+1
        if nameroadlist[j][0].endswith(road) :
            ourroad.append(nameroadlist[j])

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

def createXY(Xstart,Ystart,Xend,Yend,sumlenn,Nodefinal,Pointfinal): #หาค่า xy สับๆ
    reseultX = Xstart #จะเลื่อนไปเรื่อยๆจนถึง Xend
    reseultY = Ystart
    sumLength = sum(sumlenn)
    Pointfinal.append("P"+str(Nodefinal[0])+","+str(reseultX)+" "+str(Yend)+'\n')
    b=1
    for data in sumlenn:
        if abs(Ystart-Yend) == 0:#แนวตั้ง
            persentX = (data * abs(Xstart-Xend)) / sumLength # หาเปอเซนเทียบกับระยะห่าง xy แล้ว
            reseultX = reseultX + persentX # ได้ค่า xy ตัวใหม่ สับๆ
            Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(Yend)+'\n')
            b=b+1
            if reseultX == Xend:
                break
        elif abs(Xstart-Xend) == 0:#แนวนอน
            persentY = (data * abs(Ystart-Yend)) / sumLength
            reseultY = reseultY + persentY # ได้ค่า xy ตัวใหม่ สับๆ
            Pointfinal.append("P"+str(Nodefinal[b])+","+str(Xend)+" "+str(reseultY)+'\n')
            b=b+1
            if reseultY == Yend:
                break
        else : #แนวเฉียง
            persentX = (data * abs(Xstart-Xend)) / sumLength
            persentY = (data * abs(Ystart-Yend)) / sumLength
            reseultX = reseultX + persentX # ได้ค่า xy ตัวใหม่ สับๆ
            reseultY = reseultY + persentY # ได้ค่า xy ตัวใหม่ สับๆ
            Pointfinal.append("P"+str(Nodefinal[b])+","+str(reseultX)+" "+str(reseultY)+'\n')
            b=b+1
    if reseultY != Yend or reseultX != Xend:
        print(len(Pointfinal))
        print(b)
        Pointfinal[len(Pointfinal)-1]=("P"+str(Nodefinal[b-1])+","+str(Xend)+" "+str(Yend)+'\n')

#เหลือเอาเข้าทั้งหมดแบบtxt

def prangNode(test,filepath):
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 1
        while line:
            road=line.strip()
            test.append(str(road))
            line = fp.readline()
            cnt += 1
        #print(test)

def createOurFnodeTnode(nameroadlist,roadIDlist,roadlist,lengthlist,Fnode,Tnode,test,ourroad,OurroadFinal,FTnode,OurroadFinal1):
    a=0
    while a < len(ourroad):
        # print(nameroadlist[a][2])
        #อยาก คัดตาม node ก็เปิด
        # if str(ourroad[a][2]) in test and str(ourroad[a][3]) in test :
        #     #print (a)
        #     #roadIDlist.append(str(ourroad[a][1])+'\n')
        #     #roadlist.append(str(ourroad[a][0])+'\n')
        #     #lengthlist.append(str(ourroad[a][4])+'\n')
        #     Fnode.append(str(ourroad[a][2])+',')
        #     Tnode.append(str(ourroad[a][3])+',')
        #     #FTnode.append((ourroad[a][2],ourroad[a][3]))
        #     OurroadFinal.append((ourroad[a][0],ourroad[a][1],ourroad[a][2],ourroad[a][3],ourroad[a][4]))
        #     OurroadFinal1.append(str(ourroad[a][0])+","+str(ourroad[a][1])+","+str(ourroad[a][2])+","+str(ourroad[a][3])+","+str(ourroad[a][4])+'\n')
        # a=a+1

        Fnode.append(str(ourroad[a][2])+',')
        Tnode.append(str(ourroad[a][3])+',')
        OurroadFinal.append((ourroad[a][0],ourroad[a][1],ourroad[a][2],ourroad[a][3],ourroad[a][4]))
        OurroadFinal1.append(str(ourroad[a][0])+","+str(ourroad[a][1])+","+str(ourroad[a][2])+","+str(ourroad[a][3])+","+str(ourroad[a][4])+'\n')
        a=a+1
    #print(OurroadFinal[0][0])


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

# def MatchTxtWithLatlon(testRoadIDwithQgis,linefinal,Nodefinal,sumlenn,NodeStart,Xstart,Ystart,NodeEnd,Xend,Yend,latlonNodelist,listFromFinalStart,listFromFinalEnd,OurroadFinal2):
#     lonstart = ""
#     latstart = " "
#     lonEnd = " "
#     latEnd = " "

#     for data in latlonNodelist:
#         if NodeStart == int(data[2]):
#             lonstart = str(data[0])
#             latstart = str(data[1])
#             # listFromFinalStart.append(data[0]) # ได้ lonstart = listFromFinalStart[0] 
#             # listFromFinalStart.append(data[1]) # latstart = listFromFinalStart[1]
#         if NodeEnd == int(data[2]):
#             lonEnd = str(data[0])
#             latEnd = str(data[1])
#             # listFromFinalEnd.append(data[0]) # ได้ lonEnd = listFromFinalEnd[0] 
#             # listFromFinalEnd.append(data[1]) # ได้ latEnd = listFromFinalEnd[1] 

#     URL = "https://mmmap15.longdo.com/mmroute/json/route/raw?flon="+lonstart+"&flat="+latstart+"&tlon="+lonEnd+"&tlat="+latEnd
#     CallData = requests.get(URL)
#     datafromWWW = CallData.json() # ได้ข้อมูลทั้งหมดแล้ว
#     count = 0
#     TnodeCurrent = 0
#     while count < len(datafromWWW):
#         noterror = 0
#         for datao in OurroadFinal2:
#             if int(datafromWWW[count]['id']) == int(datao[1]):
#                 linefinal.append(str(datao[1])+",P"+str(datao[2])+",P"+str(datao[3])+","+str(datafromWWW[count]['dir'])+'\n')
#                 sumlenn.append(float(datao[4]))
#                 Nodefinal.append(datao[2])
#                 testRoadIDwithQgis.append(str(datafromWWW[count]['id'])+",")
#                 noterror = 1
#                 TnodeCurrent = int(datao[3])
        
#         if TnodeCurrent == NodeEnd:
#             Nodefinal.append(TnodeCurrent)
#             break
#         elif noterror != 1:
#             print("ทำไมroadไอดี"+str(datafromWWW[count]['id'])+"ไม่มีในdatabase")
#         count = count+1
#     print(sumlenn)




    # print(lonstart)
    # print(latstart)
    # print(lonEnd)
    # print(latEnd)
    # id = datafromWWW[1]['id']
    # print(id) 
    # print(datafromWWW)









    


        
            
            
            

            
            




        

            








        
def writetxt(file,ourroad):
    for data in ourroad :
        data = str(data)
        file.write(data)
    file.close()

def main():
    roadSort = []
    roadIDSort = []
    fnodeSort = []
    tnodeSort = []
    lenSort = []
    OurroadSort1 = []
    OurroadFinal = []
    FTnode = []
    Fnode = []
    Tnode = []
    test = []
    nameroadlist = []
    result=[]
    datafromsheet = []
    ourroad = [] #ถนนทั้งหมด เทียบถนนทั้งหมดกับชื่อถนนในtxt (ถนนที่เราเลือก)
    roadIDlist = []
    roadlist = []
    lengthlist = []
    Pointfinal = []
    linefinal = []
    OurroadFinal1 = []
    OurroadFinal2 =[]
    testRoadIDwithQgis = []
    filepath = 'nameroad1.txt' 
    file = open('testfile.txt','w')
    sql(result,nameroadlist)
    ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad)
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
    filepath = 'node.txt'         #  แปลงโหนดจากเว้นบรรทัดเป็น ,
    prangNode(test,filepath)
    file = open('node2.txt','w')
    writetxt(file,str(test)+",")
    createOurFnodeTnode(nameroadlist,roadIDlist,roadlist,lengthlist,Fnode,Tnode,test,ourroad,OurroadFinal,FTnode,OurroadFinal1)
    # file = open('roadlist.txt','w')
    # writetxt(file,roadlist)
    # file = open('roadIDlist.txt','w')
    # writetxt(file,roadIDlist)
    file = open('Tnodelist.txt','w')
    writetxt(file,Tnode)
    file = open('Fnodelist.txt','w')
    writetxt(file,Fnode)
    # print(ourroad)
    # print(len(ourroad))
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
        #print(test)
########เปลี่ยน
#-------------------------------------------------------------------
    # filepath = 'OurroadFinal.txt'     
    # with open(filepath) as fp:  
    #     line = fp.readline()
    #     while line:
    #         line=line.strip()
    #         line=line.split(",")
    #         OurroadFinal2.append((line[0],line[1],line[2],line[3],line[4]))
    #         line = fp.readline()
    # # print(OurroadFinal2)

    # latlonNodelist =[]
    # filepath = 'latlonFinishNodelist.txt'
    # with open(filepath) as fp: 
    #     line = fp.readline()
    #     while line:
    #         # count = count +1
    #         # print(count)
    #         line = line.strip()
    #         line = line.split(',')   
    #         latlonNodelist.append((line[0],line[1],line[2]))
    #         line = fp.readline()
    # print(latlonNodelist[1])


    # countLineFromFinalXY = 0
    # # nameRoadSame = []
    # # nameRoad = []
    # filepath = 'FinalXY.txt'
    # with open(filepath) as fp:  
    #     line = fp.readline() #บรรทัดแรก
    #     while line: ##
    #         listFromFinalEnd = []
    #         listFromFinalStart = []
    #         line=line.strip()
    #         line=line.split(" ")
    #         NodeStart = int(line[0])
    #         Xstart = float(line[1])
    #         Ystart = float(line[2])
    #         line = fp.readline()
    #         line=line.split(" ")
    #         NodeEnd = int(line[0])
    #         Xend = float(line[1])
    #         Yend = float(line[2])
    #         line = fp.readline() #อ่านบรรทัดที่ 3 แบบทิ้งๆไป
    #         sumlenn = []
    #         Nodefinal = []
    #         MatchTxtWithLatlon(testRoadIDwithQgis,linefinal,Nodefinal,sumlenn,NodeStart,Xstart,Ystart,NodeEnd,Xend,Yend,latlonNodelist,listFromFinalStart,listFromFinalEnd,OurroadFinal2)
    #         createXY(Xstart,Ystart,Xend,Yend,sumlenn,Nodefinal,Pointfinal)
    #         countLineFromFinalXY =countLineFromFinalXY +3
    #         print(countLineFromFinalXY)
    #         line = fp.readline()

    # file = open('finalLine.txt','w')
    # writetxt(file,linefinal)
    # file = open('finalPoint.txt','w')
    # writetxt(file,Pointfinal)
    # file = open('testRoadIDwithQgis.txt','w')
    # writetxt(file,testRoadIDwithQgis)
    #---------------------------------------------------------
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
    file = open('OurroadFinal.txt','w')
    writetxt(file,OurroadFinal1)
    #----------------------------------------------------------
    latlonNodelist =[]
    filepath = 'latlonFromNode.txt'   
    # count =0 
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            # count = count +1
            # print(count)
            line = line.strip("Point").strip()
            line=line.strip("(").strip()
            line = line.split(' ')
            latitem = line[1].split(')\t')[0] 
            nodeitem = line[1].split(')\t')[1]    
            latlonNodelist.append((str(line[0])+","+str(latitem)+","+str(nodeitem)+'\n'))
            line = fp.readline()
    file = open('latlonFinishNodelist.txt','w')
    writetxt(file,latlonNodelist)
    #------^^--แปลง txt Point (100.7110034185211731 13.99387910510712807)	1197198 เป็น lat,lon,point






if __name__=="__main__":
    main()