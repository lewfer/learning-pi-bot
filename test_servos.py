from elsi_servobonnet import *    # adafruit servo bonnet
from time import sleep

ServoBonnetFrequency(50)


servos = [ServoBonnet(2), ServoBonnet(3), ServoBonnet(4), ServoBonnet(5)]

for i in range(3):
    for servo in servos: servo.angle(45)
    sleep(1)
    for servo in servos: servo.angle(90)
    sleep(1)
    for servo in servos: servo.angle(135)
    sleep(1)

