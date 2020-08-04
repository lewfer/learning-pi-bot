# learning-pi-bot

Teaching a robot to walk using Q-learning

More details coming soon.  I'll do a tutorial on my website at some point.

## Robot construction:

Raspberry Pi Zero
Adafruit Servo Bonnet
2x servo motors
HC-SR04+ 3.3V Ulstrasonic sensor


## Code

### learnbot.py 

Contains the robot movement code.  Uses 

- joint.py
- elsi_servobonnet.py
- threadhelper.py

### learnbot_cheat.py

This encodes a simple set of movements that propel the robot forwards.  It's a cheat, because we haven't learnt these movements.  They've been encoded by a human!

### learnbot_viewpositions.py

View all the possible limb positions.

### learnbot_record_random.py

Makes random movements and records the distance moved in the movementsxx.csv file.  
If the file exists it is appended to.

### learnbot_build_r.py

Takes the movements from the movements file and creates the R matrix (outputting to R.npy) and a C matrix of counts (outputting to C.npy).  Takes all movements, unless you specify a number as a parameter

### learnbot_learn_r.py

NOT REALLY USED ANYMORE.
Runs random movements of the robot limbs, recording the distance moved (positive or negative) for each movement.  This becomes our rewards (R-table)

### learnbot_learn_q.py

Runs Q-learning on the R-table (from r.npy) to produce the Q-table.  We don't need to do this on the robot.

Uses qlearning.py.

### learnbot_move_q.py

Moves the robot according to the Q-table.  The Q-table contains the learnt patterns of bevaviour, i.e. which actions from a given state give the best/worse progression to the goal.

There are some helper shell scripts to make things easier, so you don't have to run the python code directly:

./cheat.sh   Run the human-created movements
./view.sh    View the full range of servo movements (all states)
./record.sh  Record random movements and distances
./learn.sh   Create the R matrix and then learn the Q matrix
./move.sh    Move according to the q matrix (best movements)


## Process

Set up the physical robot.  

Run learnbot_learn_r.py to learn the best individual movements.  
Run learnbot_learn_q.py to learn the best sequences.  
Run learnbot_move_q.py and the robot *should* propel itself forwards.  

You will need to experiment with physical design and the training parameters for this to work well!