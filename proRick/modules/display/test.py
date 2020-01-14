from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

lcd = CharLCD(pin_rs=18, pin_rw=23, pin_e=15, pins_data=[14, 4, 3, 2], numbering_mode=GPIO.BCM)
lcd.write_string('Hello world')
time.sleep(2)

lcd.write_string('\n\rHell Yes!!!')
time.sleep(2)
lcd.clear()