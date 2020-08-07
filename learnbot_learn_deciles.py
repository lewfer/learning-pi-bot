# Build 10 Q table from movements file
# Cuts movements file into deciles and builds a Q table for each - 10%, 20% etc.
# Can use these to show progress of training

# Import subprocess for running shell commands
import subprocess

from os import listdir, rename
from settings import *

import csv

DIVISIONS = 10

# Count lines in movements file
lines = None
with open(MOVEMENTS_FILENAME, 'r', newline='') as movementsfile:
    movementsfilereader = csv.reader(movementsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lines = list(movementsfilereader)
    lines = len(lines)

if lines is None:
    print("Nothing found in movements file")
else:   
    step = int(lines / DIVISIONS)

    percent = 0
    for build_lines in range(0, lines+1, step):
        if percent==100:
            use_lines = lines
        else:
            use_lines = build_lines
        # Learn R
        print("Learn {0}% R for {1} movements".format(percent, use_lines))
        process = subprocess.run(['python3', 'learnbot_build_r.py', str(build_lines)],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
        #print("Stdout\n", process.stdout)
        if len(process.stderr)>0:
            print("Stderr\n", process.stderr)

        # Build Q
        print("Learn {0}% Q for {1} movements".format(percent, use_lines))
        process = subprocess.run(['python3', 'learnbot_learn_q.py'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
        #print("Stdout\n", process.stdout)
        if len(process.stderr)>0:
            print("Stderr\n", process.stderr)

        # Copy generated Q table and save as appropriate decile
        rename(DATA_DIR + "/r.npy", DATA_DIR + "/r{0}.npy".format(percent))
        rename(DATA_DIR + "/c.npy", DATA_DIR + "/c{0}.npy".format(percent))
        rename(DATA_DIR + "/q.npy", DATA_DIR + "/q{0}.npy".format(percent))
        percent += 10

