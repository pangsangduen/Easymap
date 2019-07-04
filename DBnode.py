import psycopg2
import os 




con = psycopg2.connect(database = 'turntable20190613',user = 'trainee' , password='mm2019',host = '192.168.1.151' , port = '5433')
c = con.cursor()
c.execute("SELECT * FROM node")

result=c.fetchall()
print(result[0])
c.close()



