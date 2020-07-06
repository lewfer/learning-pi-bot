from time import sleep

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Set default frequency to 60hz, good for servos.
_servoBonnetFrequency = 60

def ServoBonnetFrequency(frequency):
    global _servoBonnetFrequency
    pwm.set_pwm_freq(frequency)
    _servoBonnetFrequency = frequency

# ======================================================================================================
# ServoBonnet class
# ======================================================================================================

class ServoBonnet():

    def __init__(self, pin, minPulseWidth=0.75, maxPulseWidth=2.25):
        '''Initialise the Servo on the given pin. Default frequency to 50Hz and pulse widths given in milliseconds'''
        self.pin = pin
        self.minPulseWidth = minPulseWidth
        self.maxPulseWidth = maxPulseWidth    

    def angle(self, angle):
        '''Set the servo to the given angle'''

        # Calculate the desired pulse width to achieve the angle
        pulseWidth = self.minPulseWidth + (angle * ((self.maxPulseWidth - self.minPulseWidth) / 180))
        
        # Calculate the number of "ticks", with 4096 ticks per second
        servoBonnetTicks = pulseWidth*1000/(1000*1000/4096/_servoBonnetFrequency)
        #print(servoBonnetTicks)

        # Send the pulse to the servo
        pwm.set_pwm(self.pin, 0, int(servoBonnetTicks))

    def stop(self):
        pwm.set_pwm(self.pin, 0, 0)

    def pulse(self):

        servoBonnetTicksMin = self.minPulseWidth*1000/(1000*1000/4096/_servoBonnetFrequency)
        servoBonnetTicksMax = self.maxPulseWidth*1000/(1000*1000/4096/_servoBonnetFrequency)

        '''
        for j in range(3):
            pwm.set_pwm(self.pin, 0, int(servoBonnetTicksMin))
            sleep(1)
            pwm.set_pwm(self.pin, 0, int(servoBonnetTicksMax))
            sleep(1)
        '''
            

        
        delta = int(servoBonnetTicksMax - servoBonnetTicksMin)
        print(servoBonnetTicksMin, servoBonnetTicksMax, delta)
        t = 2.0
        deltaT = t / delta

        for j in range(3):
            for i in range(delta):
                pwm.set_pwm(self.pin, 0, int(servoBonnetTicksMin+i))
                sleep(deltaT)

            for i in range(delta):
                pwm.set_pwm(self.pin, 0, int(servoBonnetTicksMin+delta-i))
                sleep(deltaT)            
        



