import os # เพราะเป็น os
import psycopg2
import math

def sql(result,nameroadlist):
    con = psycopg2.connect(database = 'turntable20190613',user = 'trainee', password = 'mm2019', host = '192.168.1.151', port = '5433')
    cur = con.cursor()
    # cur.execute("SELECT r_name_t,gid,f_node,t_node FROM road where r_char < 6 ")
    cur.execute("SELECT r_name_t,gid,f_node,t_node,length FROM road where r_char < 6 ")
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

def ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad):
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
    print(ourroad)

def  CutMap(ourroad,taaa203,gidlist,roadlist,lengthlist):
    index = 0
    numGid = 0
    while index < len(ourroad):
        road = ourroad[index][0]
        Gid = ourroad[index][1]
        lengthh = ourroad[index][4]
        roadlist.append(road+"\n")
        if road not in taaa203:
            numGid = 0
            taaa203.append(road)

        if road in taaa203:
            numGid = numGid+1
            gidlist.append(str(Gid)+",")
            lengthlist.append(str(lengthh)+"\n")
        index+= 1
    gidlist.append(numGid)
    #print(gidlist)
    print("ชื่อเส้นถนนที่หาเจอทั้งหมด  ="+str(len(taaa203)))


def GidAll(ourroad):
    ourGid = []
    index = 0
    while index < len(ourroad):
        Gid = ourroad[index][1]
        if Gid not in ourGid:
            ourGid.append(Gid)
        index+=1
    #print(ourGid)
    print("เราต้องทำ x y ทั้งหมด  ="+str(len(ourGid)))

def createXY(): #หาค่า xy สับๆ
    XYlist = [] # เส้นตรงเท่านั้น
    Xstart = 1
    Ystart = 1
    Xend = 1
    Yend = 5
    lengthAll = [10,25,50,15] # แค่ 1 ถนน
    persent = 0
    reseultX = Xstart #จะเลื่อนไปเรื่อยๆจนถึง Xend
    reseultY = Ystart
    sumLength = sum(lengthAll)
    XYlist.append((str(Xstart)+","+str(Ystart)))
    for data in lengthAll:
        if abs(Ystart-Yend) == 0:#แนวตั้ง
            persentX = (data * abs(Xstart-Xend)) / sumLength # หาเปอเซนเทียบกับระยะห่าง xy แล้ว
            reseultX = reseultX + persentX # ได้ค่า xy ตัวใหม่ สับๆ
            XYlist.append((str(reseultX)+","+str(Yend)))
            if reseultX == Xend:
                break
        elif abs(Xstart-Xend) == 0:#แนวนอน
            persentY = (data * abs(Ystart-Yend)) / sumLength
            reseultY = reseultY + persentY # ได้ค่า xy ตัวใหม่ สับๆ
            XYlist.append((str(Xend)+","+str(reseultY)))
            if reseultY == Yend:
                break
        else : #แนวเฉียง
            persentX = (data * abs(Xstart-Xend)) / sumLength
            persentY = (data * abs(Ystart-Yend)) / sumLength
            reseultX = reseultX + persentX # ได้ค่า xy ตัวใหม่ สับๆ
            reseultY = reseultY + persentY # ได้ค่า xy ตัวใหม่ สับๆ
            XYlist.append((str(reseultX)+","+str(reseultY)))
    if reseultY != Yend or reseultX != Xend:
        print("error นาจา")

def writetxt(file,ourroad):
    for data in ourroad :
        data = str(data)
        file.write(data)
    file.close()

def main():
    nameroadlist = []
    result=[]
    datafromsheet = []
    ourroad = []
    taaa203=[]
    gidlist = []
    roadlist = []
    lengthlist = []
    filepath = 'nameroad1.txt' 
    file = open('testfile.txt','w')
    sql(result,nameroadlist)
    ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad)
    CutMap(ourroad,taaa203,gidlist,roadlist,lengthlist)
    writetxt(file,ourroad)
    GidAll(ourroad)
    file = open('roadlist.txt','w')
    writetxt(file,roadlist)
    file = open('gidlist.txt','w')
    writetxt(file,gidlist)
    file = open('lengthlist.txt','w')
    writetxt(file,lengthlist)
    file = open('testplot.txt','w')
    i=0
    while i < len(ourroad) : 
        data = str(ourroad[i][2])+','+str(ourroad[i][3])+ ','
        data = str(data)
        file.write(data)
        i+=1
    



# for data1 in lines :
#      data2 = data1.split(", ")
#      listlat.append(data2[0])
#      listlon.append(data2[1])




if __name__=="__main__":
    main()