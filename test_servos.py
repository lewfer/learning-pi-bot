from elsi_servobonnet import *    # adafruit servo bonnet
from time import sleep
import sys
ServoBonnetFrequency(50)

'''
servos = [ServoBonnet(2), ServoBonnet(3), ServoBonnet(4), ServoBonnet(5)]

for i in range(3):
    for servo in servos: servo.angle(45)
    sleep(1)
    for servo in servos: servo.angle(90)
    sleep(1)
    for servo in servos: servo.angle(135)
    sleep(1)
'''
if len(sys.argv)<3:
    print("Usage: python3 test_servos.py PIN ANGLE")
else:
    servo_pin = int(sys.argv[1])
    angle = int(sys.argv[2])

    servo = ServoBonnet(servo_pin)

    servo.angle(angle)