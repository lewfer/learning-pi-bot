# Reinforcement learning using q-learning
# 
# A library to faciliate simple q-learning exercises
#
# Think Create Learn 2020

# We will use numpy because it gives us some nice functionality for arrays
import numpy as np

# Pandas gives useful functionality to export to Excel
#import pandas as pd

# For choosing random numbers
import random

# Set numpy print options to wide and print everything
np.set_printoptions(edgeitems=30, linewidth=200, threshold=np.inf)


class Matrix():
    """Representation of a 3D matrix of state, action and next_state. 
       Can be used to represent both R and Q
       """

    def __init__(self, num_states, action_names):
        """Initialise a matrix, specifying the total number of states and the names of the actions"""

        self.num_states = num_states
        self.num_actions = len(action_names)
        self.action_names = action_names

    def __str__(self):
        """String representation of the matrix is the string representation of the numpy array"""

        return str(self.matrix)

    def __repr__(self):
        """Representation of the matrix is the numpy array"""

        return repr(self.matrix)

    def createMatrix(self, value=-1):
        """Create a matrix of the right shape containing the given value in each cell"""

        self.matrix = np.full([self.num_states, self.num_actions, self.num_states], value)    

    def setMatrix(self, array):
        """Set the matrix to the passed in 3D array"""

        self.matrix = np.array(array)

    def setValue(self, state, action, next_state, value):
        """Set the value of the cell referenced by the state, action and next_state"""

        self.matrix[state, action, next_state] = value

    def getValue(self, state, action, next_state):
        """Get the value in the cell referenced by the state, action and next_state"""

        value = self.matrix[state, action, next_state]
        return value

    def maxValue(self, state):
        """Get the max value across all actions possible from the state"""

        max_value = np.max(self.matrix[state])
        return max_value

    def possibleActions(self, state):
        """Finds the possible actions from the given state"""

        # Get the row corresponding to the given state, which gives the possible next states
        row = self.matrix[state]

        # Find the states that have a reward >=0.  These are the only valid states. 
        #actions, next_states = np.where(row >= 0)  #!! for some problems -ve is invalid, but not for all
        actions, next_states = np.where(row == row)

        # Zip up tuples containing the action,next_state pairs
        return list(zip(actions, next_states))

    def bestActions(self, state):
        """Finds the best actions from the given state"""

        # Get the row corresponding to the given state, which gives the possible next states
        row = self.matrix[state]

        # Find the best (i.e. max) value in the row
        best_value = np.max(row)

        # Find the actions corresponding to the best value
        actions, next_states = np.where(row == best_value)

        # Zip up tuples containing the action,next_state pairs
        return list(zip(actions, next_states))   

    def copyFill(self, value):
        """Make a copy of the matrix and fill cells with the value"""

        new_matrix = Matrix(self.num_states, self.action_names)
        new_matrix.createMatrix(value)
        return new_matrix

    #def print(self):
    #    ""Print 
    #    print(self.matrix)

    def dumpExcel(self, filename):
        """Dump the matrix to an Excel file, one sheet per action"""
        
        with pd.ExcelWriter(filename) as writer:  
            for a in range(self.num_actions):
                data = self.matrix[:,a,:]
                pd.DataFrame(data).to_excel(writer, sheet_name=self.action_names[a])


def intersection(lst1, lst2): 
    """Utility function to find the intersection between two lists"""

    result = [value for value in lst1 if value in lst2] 
    return result 


class QAgent():
    """The QAgent is a reinforcement learning agent using Q-learning"""

    def __init__(self, R, goal_state, gamma=0.8, alpha=1):
        """Pass in your reward matrix and the goal state.  
        Gamma is the discount rate.  This is applied to the "future q", so we only take part of the reward from the future.
        Alpha is the learning rate.  Reduce alpha to make learning slower, but possibly more likely to find a solution in some cases.
        If you have no specific goal state (e.g. a walking robot) use -1."""

        self.R = R
        self.goal_state = goal_state
        self.num_states = R.num_states
        self.Q = R.copyFill(0)
        self.gamma = gamma              # discount rate
        self.alpha = alpha              # learning rate
        self.current_state = 0


    def chooseRandomAction(self):
        """Choose a random action from the possible actions from the current state"""

        # Get the possible actions from the current state
        actions = self.R.possibleActions(self.current_state)

        # Choose one at random and return it
        action = random.choice(actions)
        return action 


    def chooseBestAction(self):
        """Choose the best action from the possible actions from the current state"""

        # Get the possible actions from the current state
        possible_actions = self.R.possibleActions(self.current_state)

        # Get the best actions from the current state, i.e. the ones that give the highest q-value
        # We may get one or more with the same q-value
        best_actions = self.Q.bestActions(self.current_state)

        # Intersect the best_actions with the possible actions so we only return valid actions
        actions = intersection(possible_actions, best_actions)
        
        # Choose one of the actions at random and return it
        action = random.choice(actions)     
        return action


    def updateQ(self, action, next_state):
        """Update the Q table based on the action.  This is the key of the learning part"""

        # Find the max value in the Q row (this is the best next Q following the action)
        max_future_q = self.Q.maxValue(next_state)  
        
        current_r = self.R.getValue(self.current_state, action, next_state)
        current_q = self.Q.getValue(self.current_state, action, next_state)

        # Q learning formula - update the Q table current state with a little of the reward from the future

        # Simple version
        #new_q = int(current_r + self.gamma * max_future_q)

        # Complex version
        new_q =  ((1-self.alpha) * current_q + self.alpha * (current_r + self.gamma * max_future_q))

        # Update q table with the new value
        self.Q.setValue(self.current_state, action, next_state, new_q)        


    def train(self, num_episodes):
        """Train for the given number of episodes"""

        # Work out how often to update the user
        modcount = max(1,num_episodes/100 )

        # Run for the requested number of episodes
        for i in range(num_episodes):
            # Print out progress message
            if i%modcount==0: print("Training episode", i)

            # Choose a start state at random
            self.current_state = np.random.randint(0, self.num_states)
            #print("\nChosen random state", self.current_state)

            # Keep randomly choosing actions until we reach the goal state
            # Or if we have no goal state (-1), end the episode after one iteration
            first_time = True
            while (self.goal_state!=-1 and self.current_state != self.goal_state) or (self.goal_state==-1 and first_time):
                #print("\nCurrent state:", self.current_state)

                # Choose one of the possible actions from the current state at random
                action, next_state = self.chooseRandomAction()

                # Update the Q table based on that action
                self.updateQ(action, next_state)

                # Move to the next state
                self.current_state = next_state

                first_time = False

            # See progress in updating Q
            #if i%modcount==0:
            #print(self.Q)


    def run(self, start_state):
        """Run the search for a solution starting at the given state.  Assumes you have already trained the agent."""

        # Set the current state
        self.current_state = start_state

        # Keep a track of the path found
        path = [("Start", self.current_state)] 

        # Keep choosing actions until we reach the goal state
        while self.current_state != self.goal_state:

            # Choose the best action based on the Q table
            action, next_state = self.chooseBestAction()
            
            # Keep a track of where we've been
            path.append((self.R.action_names[action], next_state))

            # Move to the next state
            self.current_state = next_state

        # Return the chosen path
        return path

