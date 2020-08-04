# Learnbot Move Q
#
# Move the robot based on learnt behaviours
# The learnings must be specified in the Q table

# Import standard modules
import numpy as np
from time import sleep
import random

import sys
# Import core learnbot code, for robot movement
from learnbot import *

from settings import *

np.set_printoptions(suppress=True, edgeitems=30, linewidth=200, threshold=np.inf)


# Q table
# Store our learnings about good movement paths to take
# This is generated by running learnbot_learn_q.py
""" Sample Q
Q = [[  0, 911, 684, 438, 520,   0],
     [  0, 679, 850,   0,   0,   0],
     [  0,   0, 287,   0,   0, 395],
     [619, 664, 561, 481,   0,   0],
     [690, 696, 784,   0, 448, 321],
     [  0,   0, 313, 411, 553,   0]]     
"""     

Q = None



def moveNextBest(bot, state):
    """Given the current state, picks the best next state and moves to it"""

    # Get options from this state
    row = Q[state]
    #print(options)

    # Find the best (i.e. max) value in the row
    best_value = np.nanmax(row)

    # Find the actions/next states corresponding to the best value
    actions, next_states = np.where(row == best_value)    

    # If we have more than one, choose one at random
    next_state = random.choice(next_states)    

    print("Move to", next_state)

    # Move to that position
    bot.moveTo(bot.state_codes[next_state])

    return next_state

def moveNextBestWithRandomness(bot, state):
    """Given the current state, picks the next state based on a weighted favouring the the best moves"""

    # Get options from this state
    row = Q[state]
    #print("row",row)
    num_states = len(row[0])

    # Method 1: Calculate probabilities from geometric sequence
    if MOVE_CHOICE=="geom":
        # Get sort indices for these options
        sort_indices = np.argsort(row[0])
        #print("sort",sort_indices)

        # Get a geometric sequence to use to generate probabilities
        geom  = np.geomspace(1,100,num_states)
        geom_sum = sum(geom)
        #print("geom", geom)

        # Generate array with the geom sequence in the order matching the Q values
        ordered_geom = np.zeros(num_states)
        for i in range(num_states):
            r_index = sort_indices[i]
            ordered_geom[r_index] = geom[i]
        #print("ordered geom", ordered_geom)

        p = np.copy(ordered_geom)

        # Zero out any geom values where Q value is <= 0
        ltzero = np.where(row[0]<=0)[0]
        #print("ltzero", ltzero)
        np.put(p, ltzero,np.zeros(len(ltzero)))
        s = p.sum()
        if s==0:
            # We have no options, so allow moves to positions with 0 Q
            ltzero = np.where(row[0]<0)[0]
            #print("ltzero", ltzero)
            np.put(p, ltzero,np.zeros(len(ltzero)))
            s = p.sum()        
            if s==0:
                p = ordered_geom # reset
                s = p.sum()   

        # Compute the percentage from the p array
        #print("s",s)
        for i in range(num_states):
            p[i] = p[i]/s

        probs = p
                

    else:

        # Method 2: Calculate probabilities from Q values
        probs = row[0].clip(min=0)
        probs_sum = sum(probs)
        probs = probs / probs_sum

    #print("probs:", probs)

    possible_states = np.arange(num_states)
    #print("states:", possible_states)

    # Choose one at random
    next_state = np.random.choice(possible_states, p=probs)   

    print("Move to", next_state)

    # Move to that position
    bot.moveTo(bot.state_codes[next_state])

    return next_state

# Move based on learnt movements
def move():
    # Make a random initial movement
    state = bot.moveRandom()
    print("Start at", state)

    # Now loop, moving to the next best position
    while True:
        if MOVE_CHOICE=="best":
            state = moveNextBest(bot, state)
        else:
            state = moveNextBestWithRandomness(bot, state)
        sleep(MOVE_Q_WAIT_BETWEEN_MOVES)




# Main
# -------------------------------------------------------------------------------------------------

# Create the bot
bot = Learnbot(SERVOS)


# Start it up
bot.wakeSlowly(2) 

# Load the Q table - from q.npy or from name provided as a parameter
q_file = Q_FILENAME
if len(sys.argv) > 1:
    q_file = DATA_DIR + "/" + sys.argv[1]

print("Loading Q from",q_file)

# Load the Q table from file
# This was generated by the Learn Q process
try:
    Q = np.load(q_file)
    for i in range(len(Q)):
        Q[i][0][i] = -9999
except:
    print("Could not load ", q_file)
    exit()

print(Q)

# Make it move according to the learnings
move()
