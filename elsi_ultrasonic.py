import RPi.GPIO as GPIO
from time import sleep
from time import ctime
from time import time

# ======================================================================================================
# Ultrasonic class
# ======================================================================================================

class Ultrasonic():

    # Define the values we will need for ultrasonics
    SONAR_SPEED_OF_SOUND = 34300                                          # centimetres per second 
    SONAR_MAX_DISTANCE = 100                                              # centimetres  
    SONAR_MAX_WAIT = float(SONAR_MAX_DISTANCE) / SONAR_SPEED_OF_SOUND * 2 # seconds  

    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def __del__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup([self.echo, self.trigger])
        
    def echoTime(self): 
        '''
        Take a time reading from the sensor.  Returns time in seconds.
        '''

        # # Send 10us pulse to trigger the ultrasonic module
        GPIO.output(self.trigger, True)
        sleep(0.00001)
        GPIO.output(self.trigger, False)
 
        start = time()
        stop = time()
 
        # Wait for sensor to go high - pulse sent
        count=time()
        while GPIO.input(self.echo) == 0 and time()-count<Ultrasonic.SONAR_MAX_WAIT:
            start = time()
 
        # Wait for sensor to go low - echo has come back        
        count=time()
        while GPIO.input(self.echo) == 1 and time()-count<Ultrasonic.SONAR_MAX_WAIT:
            stop = time()
     
        elapsed = stop - start

        return elapsed

    def distance(self): 
        '''
        Take a distance reading from the sensor.  Returns distance in cm.
        '''

        t = self.echoTime()
    
        # Distance is time x speed of sound
        distance = t * Ultrasonic.SONAR_SPEED_OF_SOUND
        
        # That was the distance there and back so halve the value
        distance = distance / 2

        return distance  

    def medianDistance(self, n, m): 
        '''
        Read n timings and take the average of the middle m readings.  This avoids spurious readings.  Returns distance in cm.
        '''

        # Read 5 timings
        d = [0] * n
        for i in range(n):
            d[i] = self.distance()
            sleep(0.01)             # wait a little bit to let the sensor rest

        # Sort the readings and take the middle one
        d.sort()

        start = int(n/2-m/2)

        return sum(d[start:start+m]) / m



    
