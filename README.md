# Easymap

## createDatabase.py      
   - จะนำข้อมูลทั้งหมดจาก Database มาเลือกเฉพาะถนนที่มีค่า r_char < 7 

   - จากนั้นจะตัดให้ลดลงอีกโดยใช้ชื่อถนนใน `nameroad1.txt` โดยจะเลือกเฉพาะที่มีชื่อถนนตรงกัน

   - ได้ไฟล์ `OurroadFinal.txt` ซึ่งจะเก็บค่า r_name_t,roadID,F_Node,T_Node,Length

   - `latlonFromNode.txt` จะเก็บค่า [ Point (Lon Lat)	Node ]

   - จะแปลง `latlonFromNode.txt` ให้เป็น `latlonFinishNodelist.txt`

   - `latlonFinishNodelist.txt` จะเก็บค่า [ Lon,Lat,Node ]
   
   
       
## easymap2.py             
   เราจะมีไฟล์ `FinalXY.txt` ที่เก็บค่า Nodeเริ่มต้น และ Nodeสิ้นสุด ไว้เป็นคู่ๆ
    
   ### 1. def MatchTxtWithLatlon  
   - อ่านค่าจาก `FinalXY.txt` แล้วนำ Node ไป match กับไฟล์ `latlonFinishNodelist.txt` จะได้ค่า lat lon ของ Nodeเริ่มต้น และ Node สิ้นสุด

   - เอาค่า lat lon ของ Nodeเริ่มต้น และ Node สิ้นสุด ไปเรียกใช้ API จะได้ roadID ทั้งหมดจาก Nodeเริ่มต้น ถึง Node สิ้นสุด แบบที่เรียงกันเรียบร้อยแล้ว

   - เอา roadID ที่ได้มา ไป match กับ ไฟล์ `OurroadFinal.txt` เก็บค่า [ roadID , NodeStart , NodeEnd ] ในไฟล์ `finalLine.txt`

   - เก็บค่า Nodeทั้งหมด และ Lengthทั้งหมด ใส่ <list> Nodefinal และ <list> sumlenn
          
   ### 2. def createXY            
   - เอาค่า Nodeทั้งหมด และ Lengthทั้งหมด และ XYเริ่มต้น และXYสิ้นสุด(ที่ได้จาก `FinalXY.txt`) มาแบ่ง XY ตามอัตราส่วน โดยคิดอัตราส่วนจาก length ที่เก็บไว้ใน <list> sumlenn
   
   - ได้ จุดX จุดY ของ Node นั้นๆ

   - เก็บค่า Node X Y ใน <list> Pointfinal

   - ได้ `finalPoint.txt` เก็บค่า [ P+ชื่อNode , จุดX จุดY ]
          
  

