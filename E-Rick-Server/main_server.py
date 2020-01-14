import paho.mqtt.client as mqtt
import json
import time
import data_func as database
import gmaps


# MQTT Settings 
MQTT_Broker = "broker.hivemq.com"
# MQTT_Broker = "172.16.116.150"
MQTT_Port = 1883
Keep_Alive_Interval = 45
Topic_Userregister = "registerUser"
Topic_addBalance = "addBalance"
Topic_Userinfo = "stand/userinfo"
Topic_getrickshaw = "stand/getrickshaw"
Topic_Rickshaw_pickup = "rickshaw/picked"
Topic_Rickshaw_completed = "rickshaw/completed"
Topic_Rickshaw_gps = "rickshaw/gps"
Topic_Rickshaw_login = "rickshaw/login"
Topic_Rickshaw_getcustomer="rickshaw/getCustomer"
Topic_stand_ledconfig = "stand/ledconfig"
Topic_userlogin = "user/login"
Topic_driverlogin ="driver/phonelogin" 
Topic_rickshawdisconnect = "rickshaw/disconnect"
Topic_rickshawconnect = "rickshaw/connect"
Topic_rickshaw_register = "rickshaw/register"
Topic_rickshaw_passengers = "rickshaw/passengers"
Topic_send_rickshaw_loc_to_user = "user/rickshaw/loc"





#Subscribe to all Sensors at Base Topic
def on_publish(client,userdata,result):             #create function for callback
    print("data published dude")

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
    mqttc.subscribe(Topic_Rickshaw_login, 0)
    mqttc.subscribe(Topic_Rickshaw_gps,0)
    mqttc.subscribe(Topic_Userregister,0)
    mqttc.subscribe(Topic_addBalance,0)
    mqttc.subscribe(Topic_getrickshaw,0)
    mqttc.subscribe(Topic_stand_ledconfig,0)
    mqttc.subscribe(Topic_userlogin,0)
    mqttc.subscribe(Topic_rickshawdisconnect,0)
    mqttc.subscribe(Topic_rickshawconnect,0)
    mqttc.subscribe(Topic_rickshaw_passengers,0)
   

#Save Data into DB Table
def on_message(mosq, obj, msg):
	# This is the Master Call for saving MQTT Data into DB
	# For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
	# print ("MQTT Data Received...")
	# print ("MQTT Topic: " + msg.topic)  
	# print ("Data: " + str(msg.payload))
	if(msg.topic == Topic_Userinfo): 
		print("getting userinfo")
		val = msg.payload

	elif msg.topic == Topic_userlogin:
		print("checking user for logging in")
		val = msg.payload
		val = json.loads(val)
		email = str(val["email"])
		passw = str(val["pass"])
		token = str(val["token"])
		userdata = database.login_user(email,passw)
		if userdata == 0:
			mqttc.publish(Topic_userlogin+token,"0")
		else:
			userdata = json.dumps(userdata)
			mqttc.publish(Topic_userlogin+token,userdata)


	elif msg.topic==Topic_Rickshaw_completed:
		print("drive completed")
		val = msg.payload
		val = json.loads(val)
		database.set_history(str(val["time"]),str(val["rickid"]),str(val["name"]),str(val["source"]),str(val["destination"]),str(val["cardid"]),10)
		database.pay_cash(str(val[cardid]))

	elif msg.topic== Topic_rickshaw_passengers:
		print("sending passengers num")
		val = msg.payload.decode("utf-8")
		passengers=database.get_passengers_num(str(val))
		mqttc.publish(Topic_rickshaw_passengers+str(val),str(passengers))

	elif msg.topic == Topic_rickshaw_register:
		print("registering rickshaw")
		val = msg.payload
		val = json.loads(val)
		database.register_rickshaw(str(val["name"]),str(val["phone"]),str(val["ricknum"]),str(val["pass"]))


	elif msg.topic == Topic_rickshawconnect:
		print('connecting rickshaw')
		val = msg.payload.decode("utf-8")
		database.connect_rickshaw(str(val))

	elif msg.topic == Topic_rickshawdisconnect:
		print("disconnecting rickshaw")
		val = msg.payload.decode("utf-8")
		database.logout_rickshaw(str(val))
		
	elif (msg.topic == Topic_driverlogin):
		print("logging driver from phone")
		val = msg.payload
		dataa = json.loads(val)
		token = str(dataa["token"])
		passw = str(dataa["pass"])
		email = str(dataa["email"])
		result = database.get_driver_info(email,passw)
		print("dfg")
		print(str(result))
		t = Topic_driverlogin + token
		if result==0:
			mqttc.publish(t,"0")
		else:
			data = {
			"id" : result[0][0],
			"name" :result[0][1],
			"email" : result[0][2],
			"ricknum" : result[0][3],
			"phone" : result[0][4]
			}
			print(data)
			datajson = json.dumps(data)
			print(datajson)
			mqttc.publish(t,datajson)



	elif (msg.topic == Topic_getrickshaw):
		print("getting rickshaw")
		val = msg.payload
		dataa = json.loads(val)
	
		standid = str(dataa["standid"])
		print("standid = "+standid)
		destinationid = str(dataa["destinationid"])
		print("destinationid = "+destinationid)
		standloc = database.get_stand_loc(standid)
		print("getting rickshaw 3")

		pickx = standloc["x"]
		picky = standloc["y"]
		print("getting rickshaw 3")
		userdata = database.get_UserInfo(str(dataa["cardid"]))
		print("standloc : "+str(standloc))	
		print("userdata : "+str(userdata))	
		userdata["pickupdata"]=standloc
		print("getting rickshaw 3")
		if userdata:
			if userdata["balance"] >= 10:	
				ledconfig = dataa["ledconfig"]
				print("ledconfig = "+str(ledconfig))
				ledconfig[dataa["destinationid"]]+=1
				ledconfig = json.dumps(ledconfig)
				print("ledconfig json = "+str(ledconfig))
				rickdata = database.get_rickshaw(pickx,picky)
				if rickdata["id"] == -1:
					print("rickdata not available = "+str(rickdata))
					print("ok rickshaw is really not available")
					mqttc.publish(Topic_getrickshaw+str(standid),"-1")
					# mqttc.publish(Topic_stand_ledconfig+standid,leddata)
					return
				print("rickdata = "+str(rickdata))
				userdata["rickdata"]=rickdata
				destinationdata = database.get_stand_loc(dataa["destinationid"])
				userdata["destinationdata"]=destinationdata
				userjsn = json.dumps(userdata)
				print("data sending to stand and rickshaw : "+str(userjsn))
				mqttc.publish(Topic_Rickshaw_getcustomer+str(rickdata["id"]),userjsn)
				mqttc.publish(Topic_getrickshaw+str(standid),userjsn)
				database.update_stand_requests(standid,ledconfig)
			else:
				mqttc.publish(Topic_getrickshaw+str(standid),"insufficient balance")
		else:
			mqttc.publish(Topic_getrickshaw+str(standid),"user not registered")



	elif (msg.topic == Topic_Rickshaw_pickup):
		print("rickshaw picked up passenger")
		val = msg.payload
		val = json.loads(val)
		sourceid = val["source"]["id"]
		destinationid =val["destination"]["id"]
		req = database.get_stand_requests(sourceid)
		req = str(req[0])
		req = req.split("[")[1]
		req = req.split("]")[0]
		req = req.split(", ")
		for i in req:
			i = int(i)
		if req[destinationid]>0:
			req[destinationid]-=1

		req = json.dumps(req)
		database.update_stand_requests(sourceid,req)
		mqttc.publish(Topic_stand_ledconfig+sourceid,req)


	elif (msg.topic == Topic_stand_ledconfig):
		print("getting led config")
		standid = str(msg.payload.decode("utf-8"))
		print("standid " + standid)
		ledconfig = database.get_stand_requests(standid)
		print("ledconfig from database "+str(ledconfig[0]))
		
		leddata = json.dumps(ledconfig[0])
		# print("ledconfig "+str(leddata))
		mqttc.publish(Topic_stand_ledconfig+standid,leddata)


	elif (msg.topic == Topic_Userregister):
		print("registering user..")
		userjsn = msg.payload
		userdata = json.loads(userjsn)
		print("userdata "+str(userdata))
		database.register_user(userdata["cardid"],userdata["name"],userdata["email"],userdata["phone"],userdata["pass"],0)

	elif (msg.topic == Topic_addBalance):
		print("adding balance")
		val = msg.payload
		val = json.loads(val)
		cardid = val["cardid"]
		amount = val["amount"]
		database.add_balance(cardid,amount)

	elif(msg.topic == Topic_Rickshaw_gps):
		val = msg.payload
		rickdata = json.loads(val)
		rickid = rickdata["id"]
		x = rickdata["x"]
		y = rickdata["y"]
		database.update_rickshaw_loc(rickid,x,y)

	elif(msg.topic == Topic_Rickshaw_login):
		print("checking rickshaw login info")
		val = msg.payload
		dataa = json.loads(val)
		token = str(dataa["token"])
		passw = str(dataa["pass"])
		idd = str(dataa["id"])
		result = database.checkRickshawInfo(idd,passw)
		print(result)
		t = Topic_Rickshaw_login + token
		if result==0:
			mqttc.publish(t,"0")
		else:
			data = {
			"id" : result[0][0],
			"name" :result[0][1],
			"email" : result[0][2],
			"ricknum" : result[0][3],
			"phone" : result[0][4]
			}
			print(data)
			datajson = json.dumps(data)
			print(datajson)
			mqttc.publish(t,datajson)
			

	# sensor_Data_Handler(msg.topic, msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("subscribed")


try:
	mqttc = mqtt.Client()

# Assign event callbacks
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.on_publish = on_publish

	# Connect

	mqttc.connect(MQTT_Broker)


	# Continue the network loop
	mqttc.loop_forever()
	
except Exception as e:

	print(e)
	