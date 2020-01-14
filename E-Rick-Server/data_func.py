import sqlite3
import gmaps
import json

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema

def send_rickshaw_info_to_user():
	print("sending rickshaw info to user")
	TableSchema = "select id,x,y from rickshaw_active where active = 1"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()

	curs.close()
	conn.close()
	return result



def login_user(email,passw):
	print("email "+email+" pass "+passw)
	TableSchema="select * from user where email = '" + str(email)+"' and pass = "+str(passw)
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	print("result: "+str(result))
	if result:
		userdata = {
		"id":str(result[0][0]),
		"cardid" : result[0][1],
		"name" : result[0][2],
		"email" : result[0][3],
		"phone" : result[0][4],
		"balance" : str(result[0][5])
		}
		return userdata
	else:
		return 0

def set_history(time,rickid,passenger,source,destination,cardid,cost):
	TableSchema="insert into history(time,rickid,passenger,source,destination,cardid,cost) values(?,?,?,?,?,?,?)"
	val = (time,rickid,passenger,source,destination,cardid,cost)

	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema,val)
	print("saved in history")
	#Close DB
	conn.commit()
	curs.close()
	conn.close()

def pay_cash(cardid):
	TableSchema="update user set balance = balance - 10 where cardid = "+str(cardid)


	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema)
	print("cardid "+str(cardid)+" paid 10rs")
	#Close DB
	conn.commit()
	curs.close()
	conn.close()


def get_passengers_num(id):
	TableSchema = "select passengers from rickshaw_active where id = "+str(id)
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	passengers = result[0][0]
	conn.commit()
	curs.close()
	conn.close()
	return passengers

def register_rickshaw(name,phone,ricknum,passw):
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

	curs.execute("insert into rickshaw_active(id,name,phone,ricknum,active,passengers) values(?,?,?,?,?,?)",(id,name,phone,ricknum,0,0))
	curs.execute("select * from rickshaw_active")
	myresult = curs.fetchall()

	conn.commit()
	curs.close()
	conn.close()

def connect_rickshaw(id):
	TableSchema = "update rickshaw_active set active = 1 where id = "+str(id)
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)

	print("rickshaw connected "+str(id))
	conn.commit()
	curs.close()
	conn.close()

def logout_rickshaw(id):
	TableSchema = "update rickshaw_active set active = 0 where id = "+str(id)+" and passengers = 0"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	print("rickshaw disconnected ")
	conn.commit()
	curs.close()
	conn.close()


def get_driver_info(email,passw):
	TableSchema="select * from rickshaw where email = '" + str(email)+"'"
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()
	if result:
		if(result[0][5]==password):
			return result[0]
		else:
			return 0
	else :
		return 0

def get_stand_requests(standid):

	TableSchema="select requests from stand where standid = "+str(standid)


	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema)
	result = curs.fetchall()
	print("got stand requests from standid "+str(standid))
	#Close DB
	curs.close()
	conn.close()
	return result

def update_stand_requests(standid,requests):
	TableSchema="update stand set requests = '"+requests+"' where standid = "+str(standid)


	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema)
	print("stand requests updated for standid "+str(standid))
	#Close DB
	conn.commit()
	curs.close()
	conn.close()


def get_stand_loc(standid):
	TableSchema="select * from stand where standid = " + str(standid)
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()

	if result:
		standdata = {
		"x" : result[0][3],
		"y" : result[0][4],
		"name" : result[0][2],
		"id" : result[0][1]
		}
		return standdata
	else:
		return result
		

def add_balance(cardid,amount):
	TableSchema="update user set balance = balance + "+str(amount)+" where cardid = "+str(cardid)


	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema)
	print("balance added")
	#Close DB
	conn.commit()
	curs.close()
	conn.close()


def register_user(cardid,name,email,phone,pin,balance=0):
	# SQLite DB Table Schema
	TableSchema="insert into user(cardid,name,email,phone,pass,balance) values(?,?,?,?,?,?)"
	val = (cardid,name,email,phone,pin,balance)

	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	#sqlite3.complete_statement(TableSchema)
	curs.execute(TableSchema,val)
	print("user registered")
	#Close DB
	conn.commit()
	curs.close()
	conn.close()

def get_UserInfo(cardid):
	TableSchema="select * from user where cardid = " + str(cardid)
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	curs.close()
	conn.close()

	if result:
		userdata = {
		"cardid" : cardid,
		"name" : result[0][2],
		"email" : result[0][3],
		"phone" : result[0][4],
		"balance" : result[0][5]
		}
		return userdata
	else:
		return result

def checkRickshawInfo(id,password):
	TableSchema="select * from rickshaw where id = '" + id+"'"
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	
	if result:
		if(result[0][5]==password):
			curs.execute("update rickshaw_active set active = 1 where id = "+str(id))
			print("updating rikcshaw state ")
			conn.commit()
			curs.close()
			conn.close()
			return result
		else:
			curs.close()
			conn.close()
			return 0

	else :
		curs.close()
		conn.close()
		return 0


def get_rickshaw_loc():
	TableSchema = "select * from rickshaw_active where passengers = 0"
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema)
	
	result = cus.fetchall()
	result = json.dumps(result)
	curs.close()
	conn.close()
	return result

def update_rickshaw_loc(id,x,y):

	TableSchema = "update rickshaw_active set x = "+str(x)+", y = "+str(y)+" where id = "+str(id)
	TableSchema2 = "select * from rickshaw_active where id = "+str(id)
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	#Create Tables
	curs.execute(TableSchema2)
	result = curs.fetchall()
	# print("result: ",result)
	if result:
		curs.execute(TableSchema)
	else:
		TableSchema = "insert into rickshaw_active (id,x,y) values(?,?,?)"
		val = (id,x,y)
		curs.execute(TableSchema,val)

	conn.commit()
	curs.close()
	conn.close()


def get_rickshaw(desx,desy):
	minval=9999999999
	rickx = None
	ricky = None
	rickid = -1
	name = None
	phone = None
	ricknum = None
	TableSchema="select id,x,y,name,phone,ricknum from rickshaw_active where active = 1"
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()
	print ("des "+str(desx)+","+str(desy))
	#Create Tables
	curs.execute(TableSchema)
	result = curs.fetchall()
	for row in result:
		val = gmaps.get_duration_val(row[1],row[2],desx,desy)
		print("val : "+ str(val))
		if val != -1 :
			if val < minval:
				minval = val
				rickx = row[1]
				ricky = row[2]
				rickid = row[0]
				name = row[3]
				phone = row[4]
				ricknum = row[5]

	if rickid == -1 :
		for row in result:
			if row[1] and row[2]:
				rickx = row[1]
				ricky = row[2]
				rickid = row[0]
				name = row[3]
				phone = row[4]
				ricknum = row[5]




	data = {
	"id" :rickid,
	"x" : rickx,
	"y" : ricky,
	"name":name,
	"phone": phone,
	"ricknum":ricknum
	}

	curs.close()
	conn.close()
	return data
		


#Close DB
