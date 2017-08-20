import RPi.GPIO as GPIO
import time
import os

#adjust for where your switch is connected
buttonPin = 18
script = "python ./xkcdprint.py"
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)

while True:
  #assuming the script to call is long enough we can ignore bouncing
  if (GPIO.input(buttonPin)):
    #this is the script that will be called (as root)
    #os.system(script)
    print "Pressed"