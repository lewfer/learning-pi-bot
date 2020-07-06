from elsi_ultrasonic import *

uC = Ultrasonic(echo=24, trigger=23)  

for i in range(100):
    dist = uC.medianDistance(9, 3)
    print(dist)