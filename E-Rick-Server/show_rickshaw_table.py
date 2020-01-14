import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="select * from rickshaw;"



#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables

curs.execute(TableSchema)
result = curs.fetchall()

for x in result:
	print (x)

#Close DB
curs.close()
conn.close()