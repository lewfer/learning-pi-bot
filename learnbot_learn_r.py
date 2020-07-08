# Learnbot Learn R
# 
# # Learn values for R by trying out random moves and recording rewards for distance moved.

import numpy as np
#import os
from time import sleep

#from joint import *
from elsi_ultrasonic import *
#from threadhelper import *

from settings import *

from learnbot import *

import readkeys as kb


np.set_printoptions(suppress=True, edgeitems=30, linewidth=200, threshold=np.inf)

# We will use an ultrasonic sensor to record the distance moved
uC = Ultrasonic(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIGGER_PIN)    



def trainR(bot, R, C):
    '''Try random movements.  When we find a from-to movement that actually moves the robot, record it here'''

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
    print("Total movements", np.sum(C))

    # Get initial position and distance reading
    from_index = bot.moveRandom()
    last_dist = uC.medianDistance(9,3)

    # Run a few experiments
    while True:
        # Print current R
        #os.system('clear')
        print(R.round(2))

        # Get the next random movement
        to_index = bot.moveRandom()
        
        # Get the distance moved (could be negative!)
        dist = uC.medianDistance(ULTRASONIC_MEASUREMENTS_N, ULTRASONIC_MEASUREMENTS_M)
        dist_moved = dist - last_dist

        print("Moved {0}->{1}: {2}cm ({3}cm->{4}cm)".format(bot.state_codes[from_index], bot.state_codes[to_index], round(dist_moved,2), round(last_dist, 2), round(dist,2)))

        # Add distance moved to the correct cell in the matrix, and long as it's not too erratic
        if abs(dist_moved)<LEARN_R_MAX_RECORDED_MOVE:
            R[from_index, to_index] += dist_moved   # add distance in cm
            C[from_index, to_index] += 1            # increment count

        # Update indices
        last_dist = dist        # remember last distance measurement
        from_index = to_index   # remember last position

        sleep(LEARN_R_WAIT_BETWEEN_MOVES)

        # Save to file on each iteration
        np.save("r.npy", R)
        np.save("c.npy", C)

        if kb.last_key==" ":
            break


    print("Total movements", np.sum(C))        


# Main
# -------------------------------------------------------------------------------------------------

# Compute the total number of states
num_states = 1
for s in SERVOS: num_states *= len(s) 

# Rewards matrix
# Will store our learnings about good end moves
# Rows are 'from' state, columns are 'to' state
# This will be filled in in first stage of training
# R will accumulate the sum of the distance moved in each movement (from -> to state)
R = np.zeros([num_states,num_states])

# Counts matrix, keeps a count of how many times we visited the cell in the R matrix
# This is used so we can average the rewards
C = np.zeros([num_states,num_states])

# Create the bot
bot = Learnbot(SERVOS)

# Start it up
bot.wakeSlowly(2) 

# Run a background thread to check for keypresses
print("Press SPACE to stop training")
kb.startCheckKeys()

# Run the training
trainR(bot, R, C)


