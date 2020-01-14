import sys
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
import array
sys.path.append('..')
from Rickshaw import Rickshaw
import paho.mqtt.client as mqtt

sys.path.append('./modules/keypad')
import keypad
sys.path.append('./modules/buzzer')
from buzz import Buzzer
sys.path.append('./modules/button')
from button import Button
import json
import random
rickshawId = None
#sys.path.append('./modules/buzzer')
#import buzzerUse
#sys.path.append('./modules/button')
#import buttonUse
#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("-----E-Rick-----")
lcd = CharLCD(pin_rs=18, pin_rw=23, pin_e=15, pins_data=[14, 4, 3, 2], numbering_mode=GPIO.BCM)
lcd.clear()
time.sleep(0.5)
lcd.clear()
lcd.write_string('-----E-Rick-----')
time.sleep(2)
lcd.clear()

# Define Variables
#MQTT_HOST = "172.16.116.150"
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_getUserInfo = "rickshaw/getUserInfo"
MQTT_mypass = "test/mypass"
MQTT_rickshawLogin = "rickshaw/login"
MQTT_getCustomer = "rickshaw/getCustomer"
MQTT_updateLocation = "rickshaw/gps"
MQTT_pickupStatus = "rickshaw/pickup"#######################
MQTT_droppedStatus = "rickshaw/dropped"######################
MQTT_passengers = "rickshaw/passengers"
MQTT_rickshawCompleted = "rickshaw/completed"
MQTT_risckshawPicked = "rickshaw/picked"
#

rickshawId = -1
passengerCapacity = 4
rickshawInfo = None
Subscribed = False
login = False
passengers = 0
pickup = []
destination = []
currentLoc = {
        "x": 26.187182,
        "y": 91.692388}
def updateloc():
    global rickshawId
    global currentLoc
    data = currentLoc
    data ["id"] = rickshawId
    return data


def loginrickshaw():
  global token
  global rickshawId
  token = random.randint(1, 9999)
  print("token : "+str(token))
  mqttc.subscribe(MQTT_rickshawLogin+str(token),0)
  
  print("Enter id on keypad")
  lcd.clear()
  lcd.write_string('Enter id - ')
  rickshawId = keypad.getNumber(1)
  rickshawId = ''.join(str(e) for e in rickshawId)
  lcd.write_string(rickshawId)
  print(rickshawId)
  time.sleep(0.5)
  lcd.clear()
  print("\nEnter password on keypad")
  lcd.write_string("Enter pas-")
  enteredpass = [0]*4
  for i in range(4):
      enteredpass[i] = keypad.getNumber(1)
      enteredpass[i] = ''.join(str(e) for e in enteredpass[i])
      lcd.write_string(enteredpass[i])
  enteredpass = ''.join(str(e) for e in enteredpass)
  print(enteredpass)
  
  mydata = {"id":rickshawId ,
          "pass":enteredpass,
          "token":token}
 
  val = json.dumps(mydata)
 
  print(val)
  newMQTT_mypass = MQTT_mypass 
  mqttc.publish(MQTT_rickshawLogin,val)
  print("Waiting for authentication:")

def retrieveDetails(details):
    customerId = details["cardid"]
    customerName = details["name"]
    customerName = customerName.split(" ")[0]
    customerPickup = details ["pickupdata"]
    customerDestination = details ["destinationdata"]
    callTime = int(round(time.time() * 1000))
    data = details
    data["time"] = callTime
    #data = {"cardid" : customerId,
     #      "name" : customerName,
    data["source"] = customerPickup
    data["destination"] =  customerDestination
        #    "time": callTime}
    return data

def calculateNext():
    priority = [0]*8
    currtime = int(round(time.time() * 1000))
    k=300000.00
    for i in source:
        timediff = currtime - i["time"]
        priority[i["source"]["id"]] += 1
        priority[i["source"]["id"]] += float(timediff)/k
        
    for i in destination:
        timediff = currtime - i["time"]
        priority[i["destination"]["id"]] += 1
        priority[i["source"]["id"]] += float(timediff)/k
        
        ##################Add time later
    max = -1
    nextId = 0
    for i in range(8):
        if (priority > max):
            max = priority
            nextId = i
    return nextId

def onReach(reachId, mqttc):
    buzz1 = Buzzer()
    button1 = Button()
    print("Displaying information...")
    for i in destination:
        if(i["destination"]["id"] == reachId):
            lcd.clear()
            lcd.write_string("Drop - ")
            lcd.write_string("\n\r"+i["name"])
            button1.getPressedRight()
            global passengers
            passengers -= 1
            x = i
            x["rickid"]=rickshawId
            x = json.dumps(x)
            mqttc.publish(MQTT_rickshawCompleted, x)
            lcd.clear()
    for i in source:
        if(i["source"]["id"] == reachId):
            lcd.clear()
            lcd.write_string("Pickup - ")
            lcd.write_string("\n\r"+i["name"])
            button1.getPressedRight()
            data = json.dumps(i)
            mqttc.publish(MQTT_risckshawPicked, data)
            global currentLoc
            currentLoc["x"] = i["source"]["x"]
            currentLoc['y'] = i["source"]["y"]
            loc = updateloc()
            global passengers
            j = i
            source.remove(j)
            destination.append(j)
            passengers += 1
            lcd.clear()

    buzz1.notification()


try:
  def on_connect(self,mosq, obj, rc):
      print("Connected on "+MQTT_HOST)
      global Connected
      Connected = True 
  # Define on_message event function. 
  # This function will be invoked every time,
  # a new message arrives for the subscribed topic
  def on_publish(client,userdata,result):             #create function for callback
      #print("data published \n")
      pass
    
  def on_message(mosq, obj, msg):
     print ("Message Topic: " + msg.topic)
     print ("Message: " + msg.payload)
     buzz1 = Buzzer()
     if (msg.topic=="test/message"):
           print ('\nTest Message Received')
           print ("Message: " + msg.payload)
           print ("QoS: " + str(msg.qos))
           
     if (msg.topic == MQTT_rickshawLogin + str(token)):
         global login
         global rickshawId
         if (msg.payload == "0"):
             login = False
             buzz1.notification()
             print("Your password is incorrect")
             lcd.write_string('\n\rIncorrect')
             rickshawId = -1
         else:
             login = True
             print("Your password is correct")
             lcd.write_string('\n\rCorrect')
             details = msg.payload
             global rickshawInfo
             rickshawInfo = json.loads(details)
             print("Details:" + str(rickshawInfo))
             time.sleep(2)
             lcd.clear()
             lcd.write_string("Welcome")
             lcd.write_string("\n\r"+rickshawInfo["name"])
             time.sleep(2)
             lcd.clear()
         mqttc.unsubscribe(MQTT_rickshawLogin + str(token))
     if (msg.topic == MQTT_getCustomer+str(rickshawId)):
         details = msg.payload
         details = json.loads(details)
         customerName = details["name"]
         customerName = customerName.split(" ")[0]
         customerPhone = details ["phone"]
         customerPickup = details ["pickupdata"]
         customerDestination = details ["destinationdata"]
         source.append(retieveDetails(details)) 
         
     if(msg.topic == MQTT_passengers+str(rickshawId)):
         global passengers
         passengers = int(msg.payload)
         print("Number of passengers are - " + str(passengers))
         
  def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed to Topic: "+ " with QoS: " + str(granted_qos))
      
  def on_unsubscribe(client, userdata, mid):
      print("Unsubscribed from topic")          
   
  Connected= False
    # Initiate MQTT Client
  mqttc = mqtt.Client()


    # Assign event callbacks
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_subscribe = on_subscribe
  mqttc.on_publish = on_publish
  mqttc.on_unsubscribe = on_unsubscribe

    # Connect with MQTT Broker
  print ("Trying to connect...")
  mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
  
    # Continue monitoring the incoming messages for subscribed topic
  mqttc.loop_start()
    
  while Connected != True:
      time.sleep(0.1)

  while login != True:
      print("\nLogin in Now")
      loginrickshaw()
      time.sleep(1)
  print("Logged in RickshawId is :" + str(rickshawId))
  mqttc.subscribe(MQTT_passengers+str(rickshawId), 0)
  mqttc.publish(MQTT_passengers, str(rickshawId))
  mqttc.subscribe(MQTT_getCustomer+str(rickshawId), 0)
  
  onCommute = False
  button1 = Button()
  while(1):
      loc = updateloc()
      loc = json.dumps(loc)
      mqttc.publish(MQTT_updateLocation,loc)
      while(onCommute == False):
          time.sleep(1)
 
except KeyboardInterrupt:
    print ("\nCtrl+C captured, ending program.")
    lcd.clear()
    GPIO.cleanup()
    sys.exit
b