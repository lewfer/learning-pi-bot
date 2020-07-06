"""
joint.py

Implementation of Joint class.  This is where the servo control happens
"""

# Imports
# -------------------------------------------------------------------------------------------------
from elsi_servobonnet import *    # adafruit servo bonnet

# Definitions
# -------------------------------------------------------------------------------------------------
ServoBonnetFrequency(50)

# Functions
# -------------------------------------------------------------------------------------------------
def ease(t):
    return easeInOutQuad(t)

def easeLinear(t):
    return t

def easeAccelerating(t):
    return t*t*t*t

def easeInOutQuad(t):
    if t<.5:
        e = 2*t*t
    else: 
        e = -1+(4-2*t)*t
    return e

def easeInOutQuart(t):
    if t<.5:
        e = 8*t*t*t*t
    else: 
        t = t -1
        e = 1-8*(t)*t*t*t
    return e


# Class
# -------------------------------------------------------------------------------------------------
class Joint():
    '''Joint represents a single joint of a leg, controlled by a single servo motor'''

    def __init__(self, pin):
        self.pin = pin
        self.servo = ServoBonnet(pin)
        self.angle = 90                                                                 # current angle of servo
        self.defaultAngle = 90                                                          # default angle of servo
        self.stepsPerDegree = 4                                                         # number of steps to take per angular degree, bigger means smoother

    def moveTo(self, newAngle, secs):
        '''Version that keeps the time between the steps fixed but varies the angular movement'''
        #print(self.stepsPerDegree)
        waitBetweenSteps = 0
        delta = newAngle-self.angle                                                     # compute change in angle
        if abs(delta)>0 : waitBetweenSteps = float(secs)/abs(delta)/self.stepsPerDegree # compute time delay between each step
        a = self.angle                                                                  # start at the previous angle

        #print(newAngle, delta, waitBetweenSteps)

        # Move one step at a time
        tt = 0.0
        for i in range (int(abs(delta)*self.stepsPerDegree)): 
            #print(self.pin,end="")
            a = self.angle + delta * ease((i/self.stepsPerDegree)/abs(delta))           # compute angle needed to move to the next step
            #print("\t",a)
            self.servo.angle(a)                                                         # move to that angle
            #print("Move to ", a) ###
            sleep(waitBetweenSteps)
            tt += waitBetweenSteps

        #print(secs, tt)
        self.servo.angle(newAngle)                                                      # move to final angle

        # Remember the new angle
        self.angle = newAngle         

    def moveToT(self, newAngle, secs):
        '''Version that keeps the angular movement fixed and varies the time between the steps'''
        waitBetweenSteps = 0
        delta = newAngle-self.angle                                                     # compute change in angle

        #print(newAngle, delta, waitBetweenSteps)
        #print("from ", self.angle, "to", newAngle)

        # Move one step at a time
        tt = 0.0
        for i in range (int(abs(delta)*self.stepsPerDegree)): 
            #print(self.pin,end="")
            t = secs * ease((i/self.stepsPerDegree)/abs(delta))
            waitBetweenSteps = t - tt 
            #print(i, self.angle+i/self.stepsPerDegree, t, waitBetweenSteps)
            #print("\t",a)
            self.servo.angle(self.angle + i/self.stepsPerDegree * (-1 if delta < 0 else 1))                                                         # move to that angle
            #print("Move to ", a) ###
            sleep(waitBetweenSteps)
            tt += waitBetweenSteps

        print(secs, tt)
        self.servo.angle(newAngle)                                                      # move to final angle

        # Remember the new angle
        self.angle = newAngle         

    def moveRelativeToCurrent(self, delta, secs):
        '''Move relative to default angle.  newAngle can be positive or negative'''
        self.moveTo(self.angle+delta, secs)
        
    def moveRelativeToDefault(self, newAngle, secs):
        '''Move relative to default angle.  newAngle can be positive or negative'''
        self.moveTo(self.defaultAngle+newAngle, secs)

    def moveDirectTo(self, newAngle):
        self.servo.angle(newAngle)                                                      # move to final angle
        self.angle = newAngle                                                           # remember the new angle

    def moveDirectToDefault(self):
        self.moveDirectTo(self.defaultAngle)

    def updateDefault(self):
        self.defaultAngle = self.angle

    def nudgeUp(self):
        self.angle += 1
        print(self.angle)
        self.servo.angle(self.angle)                                                      # move to final angle

    def nudgeDown(self):
        self.angle -= 1
        print(self.angle)
        self.servo.angle(self.angle)                                                      # move to final angle

    def stop(self):
        #self.servo.stop()
        pass

if __name__ == "__main__":
    print("This file cannot be run directly")    


