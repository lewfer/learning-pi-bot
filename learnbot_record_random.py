# Learnbot Record Random
# 
# Make random moves and recording  distance moved.

import numpy as np
#import os
from time import sleep

#from joint import *
from elsi_ultrasonic import *
#from threadhelper import *

from settings import *

from learnbot import *

import readkeys as kb

import csv

MOVEMENTS_FILENAME = 'movements' + str(len(SERVOS)) + '.csv'

np.set_printoptions(suppress=True, edgeitems=30, linewidth=200, threshold=np.inf)

# We will use an ultrasonic sensor to record the distance moved
uC = Ultrasonic(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIGGER_PIN)    



def recordRandom(bot):
    '''Make random movements.  When we find a from-to movement that actually moves the robot, record it here'''

    # Open the movements file to record individual movements and distances
    with open(MOVEMENTS_FILENAME, 'a', newline='') as movementsfile:
        movementsfilewriter = csv.writer(movementsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #movementsfilewriter.writerow("from", "to", "distance")

        # Get initial position and distance reading
        from_index = bot.moveRandom()
        last_dist = uC.medianDistance(9,3)

        # Run a few experiments
        while True:

            # Get the next random movement
            to_index = bot.moveRandom()
            
            # Get the distance moved (could be negative!)
            dist = uC.medianDistance(ULTRASONIC_MEASUREMENTS_N, ULTRASONIC_MEASUREMENTS_M)
            dist_moved = dist - last_dist

            # Print from, to and distance 
            print("Moved {0}->{1}: {2}cm ({3}cm->{4}cm)".format(bot.state_codes[from_index], bot.state_codes[to_index], round(dist_moved,2), round(last_dist, 2), round(dist,2)))

            # Record from, to and distance to the movements file, and long as it's not too erratic
            if abs(dist_moved)<LEARN_R_MAX_RECORDED_MOVE:
                movementsfilewriter.writerow([bot.state_codes[from_index], bot.state_codes[to_index], round(dist_moved,2)])
            else:
                print("   Movement ignored - too big")

            # Update indices
            last_dist = dist        # remember last distance measurement
            from_index = to_index   # remember last position

            sleep(RECORD_WAIT_BETWEEN_MOVES)

            if kb.last_key==" ":
                break

    with open(MOVEMENTS_FILENAME,'r') as movementsfile:
        reader = csv.reader(movementsfile, delimiter = ",")
        data = list(reader)
        row_count = len(data)

        print("Total movements", row_count)        


# Main
# -------------------------------------------------------------------------------------------------


print("\nLearnbot Record Random")
print("----------------------")

# Compute the total number of states
num_states = 1
for s in SERVOS: num_states *= len(s) 

# Create the bot
bot = Learnbot(SERVOS)

# Start it up
bot.wakeSlowly(2) 

# Run a background thread to check for keypresses
print("Press SPACE to stop training")
kb.startCheckKeys()

# Run the recording
recordRandom(bot)


