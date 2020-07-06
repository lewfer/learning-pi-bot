# Learnbot Learn R
# 
# # Learn values for R by trying out random moves and recording rewards for distance moved.

import numpy as np
#import os
from time import sleep

#from joint import *
from elsi_ultrasonic import *
#from threadhelper import *

from learnbot import *

# Maximum movement that we will register (in cm)
# If more than this then we must have an error (e.g. ultrasonic sensor misreading)
MAX_RECORDED_MOVE = 8

np.set_printoptions(suppress=True)

# Rewards matrix
# Will store our learnings about good end moves
# Rows are 'from' state, columns are 'to' state
# This will be filled in in first stage of training
# We have 2 servos - Hip and Knee.  Hip H has 2 positions: 0 or 1, Knee K has 3 positions 0, 1 or 2
# So the 6 possible positions are (HK order):
# 00 01 02 10 11 12 
# R maps a 'from' (on the rows) to a 'to' (on the columns) state, so we have a 6x6 matrix
# R will accumulate the sum of the distance moved in each movement (from -> to state)
R = np.zeros([6,6])

# Counts matrix, keeps a count of how many times we visited the cell in the R matrix
# This is used so we can average the rewards
C = np.zeros([6,6])

# We will use an ultrasonic sensor to record the distance moved
uC = Ultrasonic(echo=24, trigger=23)    

# Mapping from state to code for the two joints
indices=['00','01','02','10','11','12']

def trainR():
    '''Try random movements.  When we find a from-to movement that actually moves the robot, record it here'''
    global R
    global C

    # Load previously stored R matrix, if any
    try:
        r = np.load("r.npy")
        R = r
    except:
        pass

    # Load previously stored C matrix, if any
    try:
        c = np.load("c.npy")
        C = c
    except:
        pass    
  
    
    print("R")
    print(R)  
    
    print("Counts")
    print(C)

    # Get initial position and distance reading
    from_index = bot.moveRandom()
    last_dist = uC.medianDistance(9,3)

    # Run a few experiments
    for i in range(100):
        # Print current R
        #os.system('clear')
        print(R.round(2))

        # Get the next random movement
        to_index = bot.moveRandom()
        
        # Get the distance moved (could be negative!)
        dist = uC.medianDistance(9, 3)
        dist_moved = dist - last_dist

        print("Moved {0}->{1}: {2}cm ({3}cm->{4}cm)".format(indices[from_index], indices[to_index], round(dist_moved,2), round(last_dist, 2), round(dist,2)))
        #print("Moved dist from {0} to {1} moved {2}".format(round(last_dist, 2), round(dist,2), round(dist_moved,2)))

        # Add distance moved to the correct cell in the matrix, and long as it's not too erratic
        if abs(dist_moved)<MAX_RECORDED_MOVE:
            R[from_index, to_index] += dist_moved   # add distance in cm
            C[from_index, to_index] += 1            # increment count

        # Update indices
        last_dist = dist        # remember last distance measurement
        from_index = to_index   # remember last position

        sleep(2)

        # Save to file on each iteration
        np.save("r.npy", R)
        np.save("c.npy", C)


# Main
# -------------------------------------------------------------------------------------------------

# Create the bot
bot = Learnbot()

# Start it up
bot.wakeSlowly(2) 

# Run the training
trainR()

