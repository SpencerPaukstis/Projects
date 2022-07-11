import RPi.GPIO as GPIO, time, os
from subprocess import call

DEBUG = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(5)
    
    GPIO.setup(RCpin, GPIO.IN)
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading
    
class light:
    def __init__(self, level="available!"):
        self.level = level
        
    def light_level(self, level):
        if(self.level >=3400):
            print("available!")
            call(["curl", "https://operationsfx.com/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=5&light=0"])
        else:
            self.level = "occupied!"
            print(self.level)
            call(["curl", "https://operationsfx.com/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=5&light=1"])

while True:
    input_value = RCtime(18)
    input_value = int(input_value)
    
    b = light(input_value)
    b.light = input_value
    b.light_level(input_value)
    time.sleep(5)