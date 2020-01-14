import time
import RPi.GPIO as GPIO
from keypad import keypad
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) 
if __name__ == '__main__':
    # Initialize
    kp = keypad(columnCount = 3)
    # waiting for a keypress
    digit = None
    while digit == None:
        digit = kp.getKey()
    # Print result
    print digit
    len = digit
    time.sleep(0.5)
 
    ###### 4 Digit wait ######
    seq = []
    for i in range(len):
        digit = None
        while digit == None:
            digit = kp.getKey()
        seq.append(digit)
        time.sleep(0.4)
	print(digit)
 
    # Check digit code
    print(seq)
    if seq == [1, 2, 3, '#']:
        print "Code accepted"
	GPIO.output(27,True)
    	time.sleep(5)
	GPIO.output(27,False)
