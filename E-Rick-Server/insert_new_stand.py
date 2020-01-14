import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

try:
	standid = input("standid :")
	name = input("name : ")
	loc = input("x, y coordinate ")
	
	loc = loc.split(", ")
	x = loc[0]
	y = loc[1]

	# SQLite DB Table Schema
	TableSchema='insert into stand(name,x,y,standid) values(?,?,?,?)'
	val = (name,x,y,standid)

	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema,val)
	curs.execute("select * from stand")

	myresult = curs.fetchall()

	for x in myresult:
	  print(x)

	#Close DB
	conn.commit()
	curs.close()
	conn.close()
	pass
except Exception as e:
	print(e)
