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
    
last_call = 0
light = 2

while True:
    input_value = RCtime(18)
    input_value = int(input_value)
    if input_value != 0:
        if input_value <= 3400:
            if last_call == 1 and light == 1:
                print("no change")
            else:
                light = 1
                print("Occupied")
                call(["curl", "https://operationsfx.com/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=6&light=1"])
        else:
            if last_call == 0 and light == 0:
                print("no change")
            else: 
                light = 0
                print("available")
                call(["curl", "https://operationsfx.com/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=6&light=0"])
        last_call = light    
    time.sleep(5)