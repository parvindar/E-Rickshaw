# RasPi + Grove Buzzer
import time
import RPi.GPIO as GPIO
import sys

class Buzzer:
    buzzer = 16
    def __init__(self):
        # Connect the Grove Buzzer to digital port D8
        # SIG,NC,VCC,GND
        GPIO.setmode(GPIO.BCM)
        self.buzzer = 16
        GPIO.setup(self.buzzer, GPIO.OUT)
    def notification(self):
        GPIO.output(self.buzzer,True)
        print 'start'
        time.sleep(0.5)
        # Stop buzzing for 1 second and repeat
        GPIO.output(self.buzzer,False)
        print 'stop'
        time.sleep(0.5)

if __name__ == '__main__':
    buzz1 = Buzzer()
    buzz1.notification()
    sys.exit()
    while True:
        try:
            # Buzz for 1 second
            GPIO.output(buzz.buzzer,True)
            print 'start'
            time.sleep(1)
            # Stop buzzing for 1 second and repeat
            GPIO.output(buzz.buzzer,False)
            print 'stop'
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.output(buzz.buzzer,False)
            break
        except IOError:
            print "Error"
