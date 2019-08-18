# Easymap

## createDatabase.py      
   - จะตัดDatabaseจากทั้งหมด เหลือ 200,000 กว่าตัวด้วยคำสั่ง where r_char < 7 

   - จากนั้นจะตัดให้ลดลงอีกโดยใช้ชื่อถนนใน `nameroad1.txt` โดยจะเลือกเฉพาะที่มีชื่อถนนตรงกัน

   - ได้ไฟล์ `OurroadFinal.txt` ซึ่งจะเก็บค่า ชื่อถนนTH,roadID,F_Node,T_Node,Length

   - `latlonFromNode.txt` จะเก็บค่า [ Point (Lon Lat)	Node ]

   - จะแปลง `latlonFromNode.txt` ให้เป็น `latlonFinishNodelist.txt`

   - `latlonFinishNodelist.txt` จะเก็บค่า [ Lon,Lat,Node ]
   
   
       
## easymap2.py             
   เราจะมีไฟล์ `FinalXY.txt` ที่เก็บค่า Nodeเริ่มต้น และ Nodeสิ้นสุด ไว้เป็นคู่ๆ
    
   ### 1. def MatchTxtWithLatlon  
   - พออ่านค่าเข้ามาก็จะเอา Node ไปmatchกับไฟล์ `latlonFinishNodelist.txt` จะได้ค่า lat lon ของNodeทั้งคู่

   - เอาค่า lat lon ไปใส่ใน API จะได้ roadID ทั้งหมดแบบที่เรียงกันเรียบร้อยแล้ว

   - เอา roadID ที่ได้มา ไป match กับ ไฟล์ `OurroadFinal.txt` เก็บค่า [ roadID , NodeStart , NodeEnd ] ในไฟล์ `finalLine.txt`

   - เก็บค่า Nodeทั้งหมด และ Lengthทั้งหมด ใส่ list Nodefinal และ list sumlenn
          
   ### 2. def createXY            
   - เอาค่า Nodeทั้งหมด และ Lengthทั้งหมด และ XYเริ่มต้น และXYสิ้นสุด(ที่ได้จาก FinalXY.txt) มาสับๆๆๆ XY ตาม length ที่เก็บไว้ใน list sumlenn
   
   - ได้ จุดX จุดY ของ Node นั้นๆ

   - เก็บค่า Node X Y ใน list Pointfinal

   - ได้ `finalPoint.txt` เก็บค่า [ P+ชื่อNode , จุดX จุดY ]
          
  

