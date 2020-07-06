from elsi_ultrasonic import *

from joint import *
from threadhelper import *


import random


# Class
# -------------------------------------------------------------------------------------------------
class Learnbot():
    '''Learnbot has a number of joints'''

    def __init__(self):
        self.joints = []                                                # start with no legs
        self.positions = []                                             # allowed positions of joints
        
        self.addJoint(Joint(0))
        self.addJoint(Joint(1))
        self.positions.append([170, 90]) # hip
        self.positions.append([135, 90, 0]) # knee

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

    def moveRandom(self):
        # Choose a random position for each joint
        positionA = random.randint(0, len(self.positions[0])-1)
        positionB = random.randint(0, len(self.positions[1])-1)

        # Move it
        #print("move to joint=A position=", positionA)
        #print("move to joint=B position=", positionB)
        self.moveToPosition(positionA, positionB)    

        # Get index of action in the R matrix
        index = positionB + 3*positionA

        return index

    def moveTo(self, index):
        # Choose a random position for each joint
        positionA = int(index[0])
        positionB = int(index[1])

        # Move it
        self.moveToPosition(positionA, positionB)    

        # Get index of action in the R matrix
        index = positionB + 3*positionA

        return index