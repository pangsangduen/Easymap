import os # เพราะเป็น os
import psycopg2
nameroadlist = []
con = psycopg2.connect(database = 'turntable20190613',user = 'trainee', password = 'mm2019', host = '192.168.1.151', port = '5433')
cur = con.cursor()
# cur.execute("SELECT r_name_t,gid,f_node,t_node FROM road where r_char < 6 ")
cur.execute("SELECT r_name_t,gid,f_node,t_node FROM road where r_char < 6 ")

result = cur.fetchall()
#print(result[0])
#print(len(result))


#def readfile():
i = 0
while len(nameroadlist) < len(result):
        a = result[i]
        # print(a)
        i =i+1
        nameroadlist.append(a)
        
        
# print(nameroadlist)

cur.close()

datafromsheet = []
ourroad = []
filepath = 'nameroad1.txt'  
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       road=line.strip()
       j = 0
       while j < len(nameroadlist)-1:
           j=j+1
           if nameroadlist[j][0].endswith(road) :
               ourroad.append(nameroadlist[j])
    #    print(road)
       datafromsheet.append(road)
       line = fp.readline()
       cnt += 1
# print(datafromsheet)
# print(len(datafromsheet))
# print(ourroad)
# print(len(ourroad))

taaa=[]
index = 0
for data in ourroad:
    road = ourroad[index][0]
    if road not in taaa:
        taaa.append(road)
    index+=1
print(taaa)
print(len(taaa))

file = open('testfile.txt','w')
for data in ourroad :
    data = str(data)
    file.write(data)
file.close()



# j = 0
# k = 0
# while j < len(datafromsheet) :
#     while k < len(nameroadlist):
#         if datafromsheet[j] == 


    




# for data1 in lines :
#      data2 = data1.split(", ")
#      listlat.append(data2[0])
#      listlon.append(data2[1])
