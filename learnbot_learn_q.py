'''
Reinforcement Learning

Learning Q from R
'''
import numpy as np
from qlearning import Matrix
from qlearning import QAgent

from settings import *

# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------


print("\nLearnbot Learn Q")
print("----------------")


# R table - rows are from state, cols are to state, values are average movement recorded for the transition during the Learn R process
# We only have one action (move) 
"""Sample
rewards = [ 
            [[-0.06474058,  3.12254031,  4.47118878,  0.09574791,  0.02896289, -0.14958481]],
            [[-2.44106054,  0.29848814,  5.67808946, -0.33892261, -1.13125642, -0.18263658]],
            [[-8.78985867, -6.04836014,  0.        , -0.10222197, -0.08211831,  0.        ]],
            [[ 0.05906158,  0.69738097,  2.96988885,  0.13175276, -0.01260738, -0.02589623]],
            [[ 0.55336157,  1.21644139,  5.72034121, -0.04497766,  0.03180239,  0.08109609]],
            [[-4.34466071, -2.12894281,  0.40548046,  0.03180239,  0.11357996, -0.10222197]]
          ]    
"""          

# Load the rewards table saved by the learn R process
rewards = None
try:
    r = np.load(R_FILENAME)
    rewards = r
except:
    print("Could not load r.npy")

# Load previously stored C matrix, if any
try:
    c = np.load(C_FILENAME)
    counts = c
except:
    print("Could not load c.npy")
    
# Compute mean rewards  
#with np.errstate(invalid='ignore', divide='ignore'):
#    rewards = rewards/counts
#    rewards = np.nan_to_num(rewards)

print("Rewards table loaded")
print("\nR")
print(rewards)    
print("\nC")
print(counts)     

# Put each row into a list 
# We do this because the learning process assumes there are multiple actions, but we only have one (move)
rewards = [[x] for x in rewards]

# Print out csv
"""
print("\nInput rewards:")
for row in rewards:
    for item in row[0]:
        print(str(round(item,2))+",", end="")
    print("")
"""

#input("\nPress enter to start training Q:")

# Number of states is number of rows in the rewards table
num_states = len(rewards)

# Create the R matrix
R = Matrix(num_states=num_states, action_names=['M']) # M for Move
R.setMatrix(rewards)
R.matrix = R.matrix * R_SCALE #!!  I found that sometimes scaling the rewards helped
print("\nR for training:")
print(R)

# Create a q-learning agent with no goal state and learning rate of alpha
agent = QAgent(R, goal_state=-1, alpha=1)

# Train it
print("\nTraining...")
agent.train(num_episodes=LEARN_Q_EPISODES)

# Print out Q
print("\nQ:")
for row in agent.Q.matrix:
    for item in row[0]:
        print(str(round(item,2))+",", end="")
    print("")

# Save Q matrix
np.save(Q_FILENAME, agent.Q.matrix)
