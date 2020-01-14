import sys
import RPi.GPIO as GPIO
import time
import array
sys.path.append('..')
from Stand import Stand
sys.path.append('./modules/RFID/MFRC522-python')
from mfrc522 import SimpleMFRC522
import signal
import paho.mqtt.client as mqtt
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

broker_address="172.16.116.150"
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.publish("test/message","MQTT publishing works")#publish
REQUIRED_RICKSHAW = "rickshaw/required"
MQTT_Customer = "customer"

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "\nCtrl+C captured, ending program."
    continue_reading = False
    GPIO.cleanup()
    sys.exit()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
reader = SimpleMFRC522()

stand = []
for i in range(8):
    s = Stand(i)
    stand.append(s)
    
stand[0].name='Core'
stand[1].name='Subhansiri'
stand[2].name='Siang'
stand[3].name='K.V. gate'
stand[4].name='Faculty gate'
stand[5].name='Biotech Park'
stand[6].name='Guest House'
stand[7].name='Quarters'
current_standId = 0

# Welcome message
print "Welcome to E-Rickshaw Services"
print "Press Ctrl-C to stop.\n"
print "To Call An E-Rickshaw:"
print "1) Tap your card on the RFID"
print "2) Then press the button corresponding to your destination"

def getName(uid):  #######################Get name from database
    tempName = raw_input("Enter Customer's name - ") ###############Only for testing
    return tempName
def getSource():
    return current_standId
def getDestination(): #########################Modify after button integration
    tempDestination = int(raw_input("Enter your destination id - "))
    return tempDestination
def getRickshaw(customerSource, customerDestination): ###############Calculate nearest Rickshaw
    return 1

def changeModelStand(newStand): ################Modify LEDS and current_standId
    current_standId = newStand

continue_reading = True
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    (id, text) = reader.read()
    ############client.publish('test/userinfo', str(id))
    print ("\nCard Detected")
    print ("Card UID: " + str(id))
    if(id == 633722313422):
        newst = input("What stand model do you want to see - ")
        changeModelStand(newst)
        print('\n')
        continue
    print ("Card Text: " + text)
    customerName = getName(id)
    customerSource = getSource()
    customerDestination = getDestination()
    customerRickshaw = getRickshaw(customerSource, customerDestination)
    if(customerRickshaw == -1):
        print("No Rickshaw Available")
    else:
        var = {"rickshaw":str(customerRickshaw),
               "costumer name":str(customerName),
               "standId":customerSource,
               "standname":stand[customerSource].name,
               "destinationId:":customerDestination,
               "destination:":stand[customerDestination].name }
        varjsn = json.dumps(var)
        client.publish(MQTT_Customer,varjsn)
        print("The Rickshaw assigned is - " + str(customerRickshaw))
        stand[customerSource].add_destination(customerDestination)
        print("Destinations for stand " +str(current_standId) + " are ")
        print( stand[current_standId].requests)
        print("Booked for - " + customerName)
        print("The Rickshaw is arriving at - " + stand[customerSource].name)
        print("The Rickshaw will go to - " + stand[customerDestination].name)
            