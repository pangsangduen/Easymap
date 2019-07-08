import os # เพราะเป็น os
import psycopg2

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
        print(datafromsheet)

def Ourroad(road,nameroadlist,ourroad):
    j = 0
    while j < len(nameroadlist)-1:
        j=j+1
        if nameroadlist[j][0].endswith(road) :
            ourroad.append(nameroadlist[j])

def CutRoad(ourroad,taaa203):
    index = 0
    while index < len(ourroad):
        road = ourroad[index][0]
        if road not in taaa203:
            taaa203.append(road)
        index+=1
    #print(jjj)
    #print(aaa)
    print(len(taaa203))

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
    filepath = 'nameroad1.txt' 
    file = open('testfile.txt','w')
    sql(result,nameroadlist)
    ReadtxtToList(filepath,datafromsheet,nameroadlist,ourroad)
    CutRoad(ourroad,taaa203)
    writetxt(file,ourroad)

if __name__=="__main__":
    main()