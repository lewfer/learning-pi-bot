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

    for build_lines in range(10, lines+1, step):
        # Learn R
        print("Learn R for", build_lines, "movements")
        process = subprocess.run(['python3', 'learnbot_build_r.py', str(build_lines)],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
        print("Stdout\n", process.stdout)
        print("Stderr\n", process.stderr)

        # Build Q
        print("Build Q for", build_lines, "movements")
        process = subprocess.run(['python3', 'learnbot_learn_q.py'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
        print("Stdout\n", process.stdout)
        print("Stderr\n", process.stderr)

        rename("data/q.npy", "data/q{0}.npy".format(build_lines))

