import numpy as np

try:
    r = np.load("r.npy")
except:
    print("Could not load r.npy")

# Load previously stored C matrix, if any
try:
    c = np.load("c.npy")
except:
    print("Could not load c.npy")

try:
    q = np.load("q.npy")
except:
    print("Could not load q.npy")


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
r = r/c
r= np.nan_to_num(r)
    
print("\n\nMean R:")
printMatrix(r)


print("\n\nQ:")
printQ(q)