import time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)

class Button:
    ledLeft = 12
    ledRight = 7
    def __init__(self):
        # Connect the Grove Buzzer to digital port D8
        # SIG,NC,VCC,GND
        GPIO.setmode(GPIO.BCM)
        self.ledLeft = 12
        self.ledRight = 7
        GPIO.setup(self.ledLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
        GPIO.setup(self.ledRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23

    def getPressedRight(self):
        button_state = True
        while button_state:
            time.sleep(0.2)
            button_state = GPIO.input(self.ledRight)
        print("Pressed Right")
        return 1
    def getPressedLeft(self):
        button_state = True
        while button_state:
            time.sleep(0.2)
            button_state = GPIO.input(self.ledLeft)
        print("Pressed Left")
        return 1
    def ifPressedLeft(self):
        button_state = GPIO.input(self.ledLeft)
        if button_state == False:
            return True
        else:
            return  False  
        

if __name__ == '__main__':
    but1 = Button()
    but1.getPressedLeft()
    but1.getPressedRight()

