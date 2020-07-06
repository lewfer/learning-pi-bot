# Move based on learnt behaviours


import numpy as np
import os
import random
from time import sleep

from joint import *
from elsi_ultrasonic import *
from threadhelper import *


np.set_printoptions(suppress=True)

# Rewards matrix
# Will store our learnings about good end moves
# Rows are 'from' state, columns are 'to' state
# This will be filled in in first stage of training
# We have 2 servos - Hip and Knee.  Hip H has 2 positions: 0 or 1, Knee K has 3 positions 0, 1 or 2
# So the 6 possible positions are (HK order):
# 00 01 02 10 11 12 
# R maps a 'from' to a 'to' state, so we have a 6x6 matrix
R = np.zeros([6,6])

C = np.zeros([6,6])

# Q matrix
# Will store our learnings about good movement paths to take
# This ill be filled in in the second stage of training
Q = np.zeros([6,6])


# Gamma (learning parameter).
gamma = 0.8

uC = Ultrasonic(echo=24, trigger=23)    

# Class
# -------------------------------------------------------------------------------------------------
class Learnbot():
    '''Learnbot has a number of joints'''

    def __init__(self):
        self.joints = []                                                # start with no legs
        self.positions = []                                             # allowed positions of joints

    def addJoint(self, joint):
        '''Add joints'''
        self.joints.append(joint)

    def moveToDefaultPosition(self):  
        '''Move all joints to their default position.  This moves all servos instantly to their default positions.
           This can cause a high current draw which shuts down the Pi.''' 

        for j in range(len(self.joints)):
            self.joints[j].moveDirectToDefault()

    def wakeSlowly(self, t=5):
        '''Move all legs slowly to their default position.  The slow wake prevents a surge in current draw that could shut down the Pi.'''
       
        for j in range(len(self.joints)):
            self.joints[j].moveRelativeToDefault(0, t/4)

    def legsUp(self):
        self.joints[0].moveTo(newAngle=0, secs=0.2)
        self.joints[1].moveTo(newAngle=0, secs=0.2)

    def moveJoint(self, jointNo, position):
        pass

    def moveToPosition(self, positionA, positionB):
        threadA = Thread(target=self.joints[0].moveTo, kwargs={"newAngle":self.positions[0][positionA], "secs":1})
        threadB = Thread(target=self.joints[1].moveTo, kwargs={"newAngle":self.positions[1][positionB], "secs":1})
        runThreadsTogether([threadA,threadB])

        #self.joints[0].moveTo(newAngle=self.positions[0][positionA], secs=1)
        #self.joints[1].moveTo(newAngle=self.positions[1][positionB], secs=1)




# Move based on learnt movements
def move():

    global R
    global C

    try:
        r = np.load("r.npy")
        R = r
    except:
        pass

    try:
        c = np.load("c.npy")
        C = c
    except:
        pass    
  
    print("Counts")
    print(C)
    print(R)  

    R = R/C
    R = np.nan_to_num(R)
    print(R) 

    index = moveRandom(bot)
    while True:
        index = moveNextBest(bot, index)
        sleep(3)


def trainQ():
    pass



# Main

# Create the bot
bot = Learnbot()
bot.addJoint(Joint(0))
bot.addJoint(Joint(1))
bot.positions.append([150, 90]) # hip
bot.positions.append([135, 90, 0]) # knee

# Start it up
bot.wakeSlowly(2) 

move()
