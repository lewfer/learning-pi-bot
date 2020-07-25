"""
Learnbot
 
A class to provide generic functionality for a learning robot.
This class doesn't do the learning.  It just represents the state of the robot and moves it.

Usage:

Import this library:
    from learnbot import *

Create the bot.  Here we specify 3 servos.  The first has 2 positions, the second has 3 positions and the third has 3 positions
    bot = Learnbot([[170, 90], [135, 90, 0], [20,60, 100]])

Start it up
    bot.wakeSlowly(2) 
 
Move it
    bot.moveTo('001') # move servos to 170, 135 and 60 respectively
    bot.moveTo('022')# move servos to 170, 135 and 60 respectively

"""

#from elsi_ultrasonic import *

from joint import *
from threadhelper import *
import random

from settings import *

# Class
# -------------------------------------------------------------------------------------------------
class Learnbot():
    '''Learnbot has a number of joints'''

    def __init__(self, joints):
        '''Joints is list of lists.  The outer list contains one list per joint.  The inner list contains the angles allowed for each joint'''

        # Initialise an empty list of joints and joint angles
        self.joints = []
        self.angles = [] 
        
        self.num_joints = len(joints)

        # Add the joints and angles to the arrays
        pin = SERVO_PIN_START
        self.num_states = 1
        for angles in joints:
            self.joints.append((Joint(pin)))
            self.angles.append(angles)
            self.num_states *= len(angles)
            pin += 1

        print("Learnbot")

        # Confirm number of states
        print("Num states", self.num_states)

        # Generate a list of state codes
        self.state_codes = [self.stateToCode(state) for state in range(self.num_states)]
        print("State codes:", self.state_codes)

        print()

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
        '''Lift all the legs up - NOT TESTED'''
        for joint in self.joints:
            joint.moveTo(newAngle=0, secs=JOINT_MOVE_SECS)

    def moveToPosition(self, positions):
        '''Move servos to the positions given.  Positions is a list of the positions in the positions list'''

        # Create a thread for each joint movement, so we can move all joints together
        threads = []
        for joint in range(len(positions)):
            position = positions[joint]
            threads.append(Thread(target=self.joints[joint].moveTo, kwargs={"newAngle":self.angles[joint][position], "secs":JOINT_MOVE_SECS}))
            #threads.append(Thread(target=self.joints[joint].moveDirectTo, kwargs={"newAngle":self.angles[joint][position]}))

        # Move all joints together
        runThreadsTogether(threads)

    def moveRandom(self):
        '''Move all servos to a random position'''

        # Choose a random position for each joint
        random_positions = []
        for angles in self.angles:
            position = random.randint(0, len(angles)-1)
            random_positions.append(position)

        # Move servos to positions
        self.moveToPosition(random_positions)  

        # Get state index from the positions of each joint
        state = self.state(random_positions)

        return state

    def moveTo(self, positions_code):
        """Code is the coded positions, e.g. 12 means move first servo to position 1 and second servo to position 2"""

        # Requested positions
        requested_positions = self.codeToPositions(positions_code)

        # Move it
        self.moveToPosition(requested_positions)    

        # Get state index from the positions of each joint
        state = self.state(requested_positions)

        return state

    def codeToPositions(self, positions_code):
        """Convert the code to a list of positions.  E.g. "12" returns [1,2]"""

        # Pull out positions from the code
        requested_positions = []
        for i in range(len(positions_code)):
            this_position = int(positions_code[i])
            requested_positions.append(this_position)
        return requested_positions

    def stateToCode(self, state):
        """Convert the state to a code.  E.g. state 1 could be "01", depending on the servo setup"""

        multiplier = 1
        code = ""
        for i in range(self.num_joints-1, -1, -1):
            num_angles = len(self.angles[i])
            code += str(int((state / multiplier ) % num_angles))
            multiplier *= len(self.angles[i])

        # Return the reversed code
        return code [::-1]


    def state(self, positions):
        '''Get the unique state index from the list of servo positions.  E.g. [0,2,1] might be state 7'''

        #print(positions)
        # Get state from the positions of each joint
        multiplier = 1
        state = 0
        for i in range(self.num_joints-1, -1, -1):
            state += positions[i]*multiplier
            multiplier *= len(self.angles[i])

        return state