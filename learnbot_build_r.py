# Learnbot Build R
# 
# Takes movements from the movements file and creates the R and C matrix

import numpy as np
from time import sleep

from settings import *

from learnbot import *


import csv

MOVEMENTS_FILENAME = 'movements' + str(len(SERVOS)) + '.csv'


np.set_printoptions(suppress=True, edgeitems=30, linewidth=200, threshold=np.inf)



def trainR(bot, R, C, num_movements):
    '''Read movements from the file'''

    # Open the movements file 
    with open(MOVEMENTS_FILENAME, 'r', newline='') as movementsfile:
        movementsfilewriter = csv.writer(movementsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        movementsfilereader = csv.reader(movementsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        lines = list(movementsfilereader)
        
        for line in lines[:min(num_movements,len(lines))]:
            from_index = bot.state(bot.codeToPositions(line[0]))
            to_index = bot.state(bot.codeToPositions(line[1]))
            dist_moved = float(line[2])

            print(from_index, to_index, dist_moved)

            if abs(dist_moved)<LEARN_R_MAX_RECORDED_MOVE:
                #R[from_index, to_index] += dist_moved   # add distance in cm
                C[from_index, to_index] += 1            # increment count

                R[from_index, to_index].append(dist_moved)

        # Take mean of 
        print(R)
        R = np.vectorize(lambda x: np.median(x))(R)


    print(R)
    # Save to file on each iteration
    np.save("r.npy", R)
    np.save("c.npy", C)



# Main
# -------------------------------------------------------------------------------------------------

print("\nLearnbot Build R")
print("----------------")

# Compute the total number of states
num_states = 1
for s in SERVOS: num_states *= len(s) 

# Rewards matrix
# Will store our learnings about good end moves
# Rows are 'from' state, columns are 'to' state
# This will be filled in in first stage of training
# R will accumulate the sum of the distance moved in each movement (from -> to state)
#R = np.zeros([num_states,num_states])

# Counts matrix, keeps a count of how many times we visited the cell in the R matrix
# This is used so we can average the rewards
C = np.zeros([num_states,num_states])

R = np.empty(num_states*num_states, dtype=np.object)
for i in range(R.shape[0]):
    R[i] = []
R = R.reshape(num_states,num_states)

# Create the bot
bot = Learnbot(SERVOS)

# Start it up
bot.wakeSlowly(2) 

num_movements = int(input("How many movements to include?"))

# Run the training
trainR(bot, R, C, num_movements)


