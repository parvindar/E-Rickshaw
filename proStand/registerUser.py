import sys
sys.path.append('./modules/RFID/MFRC522-python')
from mfrc522 import SimpleMFRC522
import paho.mqtt.client as mqtt
import json

# Define Variables
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45

client = mqtt.Client("P1") #create new instance
client.connect(MQTT_HOST) #connect to broker

print("Scan your card on RFID reader.")
reader = SimpleMFRC522()
(id, text) = reader.read()

name = raw_input("Enter your name - ")
email = raw_input("Enter your email - ")
phone = raw_input("Enter your Phone number - ")
passw = raw_input("Enter a password:")

userdata = {
    "name":name,
    "email":email,
    "phone":phone,
    "pass": passw,
    "cardid":id}
userjsn = json.dumps(userdata)
client.publish("registerUser",userjsn)#publish