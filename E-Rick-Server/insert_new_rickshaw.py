import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

name = input("name : ")
phone = input("phone : ")
ricknum = input("rickshaw number : ")
passw = input("pass : ")

# SQLite DB Table Schema
TableSchema="insert into rickshaw(name,phone,ricknum,pass) values(?,?,?,?)"
val = (name,phone,ricknum,passw)

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
#sqlite3.complete_statement(TableSchema)
curs.execute(TableSchema,val)
curs.execute("select id from rickshaw where name = '"+name+"' and phone = "+str(phone))
myresult = curs.fetchall()

id = myresult[0][0]

print(id)


curs.execute("insert into rickshaw_active(id,name,phone,ricknum,active,passengers) values(?,?,?,?,?,?)",(id,name,phone,ricknum,0,0))

curs.execute("select * from rickshaw_active")
myresult = curs.fetchall()

for x in myresult:
  print(x)

#Close DB

conn.commit()
curs.close()
conn.close()