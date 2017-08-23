import RPi.GPIO as GPIO
import time
import os

#adjust for where your switch is connected
buttonPin = 24
script = "python ./xkcdprint.py -r"
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if (GPIO.input(buttonPin) == 0):
        os.system(script)
        time.sleep(1)
