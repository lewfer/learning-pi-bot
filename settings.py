# SERVOS: Set up our servos.  The outer array has one item per servo.  The inner arrays have one item per servo position.  The values are the servo angles.
# SERVO_PIN_START: Number of first pin used on servo bonnet.  Assumes sequence from that pin

# Use these settings for single claw operation
SERVOS = [[170, 90], [135, 90, 0]]
SERVO_PIN_START = 0


# Use these settings for 4-legged operation
#SERVOS = [[90,50], [90,130], [90,50], [90,130]]
#SERVOS = [[130,50], [50,130], [130,50], [50,130]]
#SERVOS = [[110,70], [70,130], [110,70], [70,110]]
#SERVO_PIN_START = 2

# Use these settings for 4-legged + weight operation
#SERVOS = [[130,50], [50,130], [130,50], [50,130], [20, 160]]
#SERVO_PIN_START = 2


# Number of seconds for each joint movement
JOINT_MOVE_SECS = 0.2

 
# Raspberry Pi pins where ultrasonic sensor is
ULTRASONIC_ECHO_PIN = 24
ULTRASONIC_TRIGGER_PIN = 23

# The number of measurements (N) and middle values (M) to take
# Final reading is mean of the M middle readings from N
ULTRASONIC_MEASUREMENTS_N = 9
ULTRASONIC_MEASUREMENTS_M = 3

# Scale factor to apply to R before Q learning
R_SCALE = 10

LEARN_Q_EPISODES = 2000

# Maximum movement that we will register (in cm) when learning R
# If more than this then we must have an error (e.g. ultrasonic sensor misreading)
LEARN_R_MAX_RECORDED_MOVE = 20

# Number of seconds to wait between movements
RECORD_WAIT_BETWEEN_MOVES = 1

# Number of seconds to wait between movements
MOVE_Q_WAIT_BETWEEN_MOVES = 1