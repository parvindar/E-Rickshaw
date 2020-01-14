import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class LED:
    led = [0]*8
    led[0] = 26
    led[1] = 19
    led[2] = 13
    led[3] = 6
    led[4] = 5
    led[5] = 22
    led[6] = 27
    led[7] = 17

    for i in range(8):
        GPIO.setup(led[i], GPIO.OUT)  #LED to GPIO24
    
    def clear(self):
        for i in range(8):
            GPIO.output(self.led[i], False)
    def update(self, arr):
        for i in range(8):
            if(arr[i] > 0):
                GPIO.output(self.led[i], True)
    
