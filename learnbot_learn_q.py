'''
Reinforcement Learning

Learning Q from R
'''

from qlearning import Matrix
from qlearning import QAgent

# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------

# R matrix - rows are from state, cols are to state, -1 means not allowed, 0 means allowed, 100 means reached goal
# We only have one action (move) 
rewards = [ 

 [[-0.06474058,  3.12254031,  4.47118878,  0.09574791,  0.02896289, -0.14958481]],
 [[-2.44106054,  0.29848814,  5.67808946, -0.33892261, -1.13125642, -0.18263658]],
 [[-8.78985867, -6.04836014,  0.        , -0.10222197, -0.08211831,  0.        ]],
 [[ 0.05906158,  0.69738097,  2.96988885,  0.13175276, -0.01260738, -0.02589623]],
 [[ 0.55336157,  1.21644139,  5.72034121, -0.04497766,  0.03180239,  0.08109609]],
 [[-4.34466071, -2.12894281,  0.40548046,  0.03180239,  0.11357996, -0.10222197]]

          ]    

# Create the R matrix
R = Matrix(num_states=6, action_names=['M'])
R.setMatrix(rewards)
R.matrix = R.matrix * 100
print("\nR:")
print(R)

# Create a q-learning agent
agent = QAgent(R, goal_state=-1, alpha=1)

# Train it
print("\nTraining...")
agent.train(num_episodes=100)

print("\nQ:")
print(agent.Q) 

#np.save("q.npy", agent.Q)
