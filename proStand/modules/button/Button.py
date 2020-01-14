import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
class Button:
    but = [0]*8
    but[0] = 21
    but[1] = 20
    but[2] = 16
    but[3] = 12
    but[4] = 7
    but[5] = 24
    but[6] = 23
    but[7] = 18

    for i in range(8):
        GPIO.setup(but[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
    
    def getPressedId(self):
        while True:
            for i in range(8):
                button_state = GPIO.input(self.but[i])
                if(button_state == False):
                    return i
            time.sleep(0.2)
