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

### learnbot_learn_r.py

Runs random movements of the robot limbs, recording the distance moved (positive or negative) for each movement.  This becomes our rewards (R-table)

### learnbot_learn_q.py

Runs Q-learning on the R-table to produce the Q-table.  We don't need to do this on the robot.

Uses qlearning.py.

### learnbot_move_q.py

Moves the robot according to the Q-table.  The Q-table contains the learnt patterns of bevaviour, i.e. which actions from a given state give the best/worse progression to the goal.


## Process

Set up the robot.  Run learnbot_learn_r.py to learn the best individual movements.  Take the R-table produced and plug it into learnbot_learn_q.py.  Run this.  Take the Q-table produced and plug it into learnbot_move_q.py.  Run this and the robot *should* propel itself forwards.  

You will need to experiment with physical design and the training parameters for this to work well!