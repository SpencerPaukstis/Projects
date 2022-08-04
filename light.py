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
light = 0
count_on = 0
count_off = 0

while True:
   
    input_value = input_value = RCtime(18)
    #input_value = int(input_value)
    
    if input_value <= 3400:
        if last_call == 1 and light == 1:
            print("no change")
            count_on += 1
        else:
            light = 1
            print("Occupied")
            call(["curl","-k", "https://us-east1-webfx-tech-enablement.cloudfunctions.net/operationsfx-rest/api/v2/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=8&light=1", "--header", "x-api-key: f48fa7b3-9522-4e80-b6a1-6671541969cf"])
            count_on = 1
            count_off = 0
    else:
        if last_call == 0 and light == 0:
            print("no change")
            count_off += 1
        else:
            light = 0
            print("available")
            call(["curl","-k", "https://us-east1-webfx-tech-enablement.cloudfunctions.net/operationsfx-rest/api/v2/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=8&light=0", "--header", "x-api-key: f48fa7b3-9522-4e80-b6a1-6671541969cf"])
            count_on = 0
            count_off = 1

    if count_on == 60:
        print("5 min passed...updating api to on")
        call(["curl","-k", "https://us-east1-webfx-tech-enablement.cloudfunctions.net/operationsfx-rest/api/v2/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=8&light=1", "--header", "x-api-key: f48fa7b3-9522-4e80-b6a1-6671541969cf"])
        count_on = 0
    if count_off == 60:
        print("5 min passed...updating api to off")
        call(["curl","-k", "https://us-east1-webfx-tech-enablement.cloudfunctions.net/operationsfx-rest/api/v2/facilities/api/light?auth=f48fa7b3-9522-4e80-b6a1-6671541969cf&id=8&light=0", "--header", "x-api-key: f48fa7b3-9522-4e80-b6a1-6671541969cf"])
        count_off = 0
   
    last_call = light

    time.sleep(5)