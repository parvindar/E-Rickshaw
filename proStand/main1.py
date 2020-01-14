import sys
import RPi.GPIO as GPIO
import time
import array
sys.path.append('..')
import paho.mqtt.client as mqtt
sys.path.append('./modules/RFID/MFRC522-python')
from mfrc522 import SimpleMFRC522
sys.path.append("./modules/button")
from Button import Button
sys.path.append("./modules")
from led import LED
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.OUT)  #LED to GPIO2 for available led
GPIO.output(2, False)

print("-----E-Stand-----")
led1 = LED()
led1.clear()

# Define Variables
#MQTT_HOST = "172.16.116.150"
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_getLED = "stand/ledconfig"
MQTT_getRickshaw = "stand/getrickshaw"
#

standid = -1
ledArr = [0]*8
pressed = 0
try:
  def on_connect(self,mosq, obj, rc):
      print("Connected on "+MQTT_HOST)
      global Connected
      Connected = True 
  # Define on_message event function. 
  # This function will be invoked every time,
  # a new message arrives for the subscribed topic
  def on_publish(client,userdata,result):             #create function for callback
      print("data published \n")
    
  def on_message(mosq, obj, msg):
     global standid
     global ledArr
     print ("Message Topic: " + msg.topic)
     print ("Message: " + msg.payload)
     if (msg.topic=="test/message"):
           print ('\nTest Message Received')
           print ("Message: " + msg.payload)
     if (msg.topic==MQTT_getRickshaw+str(standid)):
           print ('\nStand Message Received')
           print ("Message: " + msg.payload)
           val = msg.payload.decode("utf-8")
           if val == "-1":
               print("no rickshaw available dude")
               for i in range(5): 
                   GPIO.output(2, True)
                   time.sleep(0.5)
                   GPIO.output(2, False)
                   time.sleep(0.3)
           else:
               global ledArr
               ledArr[pressed] += 1
               led1.update(ledArr)
               
     if (msg.topic==MQTT_getLED+str(standid)):
           print ('\nLED Details Received')
           received = msg.payload
           if(str(received) == '[null]'):
               ledArr = [0]*8
               led1.update(ledArr)
           else:
               received = json.loads(received)
               ledArr = received[0]
               ledArr = ledArr.split("[")[1]
               ledArr = ledArr.split("]")[0]
               ledArr = ledArr.split(", ")
               for i in range(8):
                   ledArr[i] = int(ledArr[i])
               print("ledArr: "+ str(ledArr))
               led1.update(ledArr)

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
  
  button1 = Button()
  print("\nPress the button corresponding to the stand model you want to see:")
  pressed = button1.getPressedId()
  standid = pressed
  mqttc.subscribe(MQTT_getLED+str(standid), 0)
  mqttc.publish(MQTT_getLED, str(standid))
  print("Showing the map at stand location - "+ str(standid))
  mqttc.subscribe(MQTT_getRickshaw+str(standid), 0)
  print("-----------------------------------")
 # Welcome message
  print "\nWelcome to E-Rickshaw Services"
  print "Press Ctrl-C to stop.\n"
  print "To Call An E-Rickshaw:"
  print "1) Tap your card on the RFID"
  print "2) Then press the button corresponding to your destination"


  def getSourceId():
      global standid
      return standid
  def getDestinationId():
      print("Press your destination id - ")
      global pressed
      pressed = button1.getPressedId()
      print("Your destination is set to - " + str(pressed))
      return pressed
  def getRickshaw():##################get assigned rickshaw from server
      return 1
  # Create an object of the class MFRC522
  reader = SimpleMFRC522()

  while(1):
      (id, text) = reader.read()
      print ("\nCard Detected")
      print ("Card UID: " + str(id))
      print ("Card Text: " + text)
      customerSourceId = getSourceId()
      customerDestinationId = getDestinationId()
      customerRickshaw = getRickshaw()
      if(customerRickshaw == -1):
        print("No Rickshaw Available")
      else:
        var = {"cardid":id,
               "standid":customerSourceId,
               "destinationid":customerDestinationId,
               "ledconfig":ledArr}
        varjsn = json.dumps(var)
        mqttc.publish(MQTT_getRickshaw,varjsn)
 
except KeyboardInterrupt:
    print ("\nCtrl+C captured, ending program.")
    GPIO.cleanup()
    sys.exit()
    

    
