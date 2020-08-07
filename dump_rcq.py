import numpy as np
from settings import *

import sys

r_file = R_FILENAME
if len(sys.argv) > 1:
    r_file = DATA_DIR + "/r" + sys.argv[1] + ".npy"

c_file = C_FILENAME
if len(sys.argv) > 1:
    c_file = DATA_DIR + "/c" + sys.argv[1] + ".npy"

q_file = Q_FILENAME
if len(sys.argv) > 1:
    q_file = DATA_DIR + "/q" + sys.argv[1] + ".npy"

errors = False

try:
    print("Loading", r_file)
    r = np.load(r_file)
    r = np.nan_to_num(r)
except:
    print("Could not load", r_file)
    errors = True

# Load previously stored C matrix, if any
try:
    print("Loading", c_file)
    c = np.load(c_file)
except:
    print("Could not load", c_file)
    errors = True

try:
    print("Loading", q_file)
    q = np.load(q_file)
except:
    print("Could not load", q_file)
    errors = True

if errors:
    exit()

def printMatrix(mat):
    # Print out csv
    for row in mat:
        for item in row:
            print(str(round(item,2))+",", end="")
        print("")

def printQ(mat):
    # Print out csv
    for row in mat:
        for item in row[0]:
            print(str(round(item,2))+",", end="")
        print("")




print("\n\nR:")
printMatrix(r)

print("\n\nC:")
printMatrix(c)

# Compute mean rewards  
"""
print("\n\nMean R:")
with np.errstate(invalid='ignore', divide='ignore'):
    r = r/c
    r= np.nan_to_num(r)
    printMatrix(r)
"""

print("\n\nQ:")
printQ(q)

print("\nTotal movements",c.sum())