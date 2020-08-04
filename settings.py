# SERVOS: Set up our servos.  The outer array has one item per servo.  The inner arrays have one item per servo position.  The values are the servo angles.
# SERVO_PIN_START: Number of first pin used on servo bonnet.  Assumes sequence from that pin

# Modes
MODE_ONE_CLAW = 0               # one claw at front with 2 servos
MODE_TWO_LEGS = 1               # two legs with 2 servos each
MODE_FOUR_SIMPLE_LEGS = 2       # four legs with one servo each

# Selected mode - set to one of the above
MODE = MODE_ONE_CLAW

if MODE==MODE_ONE_CLAW:
    MODE_NAME = "one_claw"
    # Use these settings for single claw operation
    # Hip 0 is all the way up, 180 is all the way down
    # Knee 0 if towards body, 180 is away from body
    #          hip         knee  
    #          down  up    forward centre back
    SERVOS = [[130,  70], [135,    90,    0]]
    SERVO_PIN_START = 0

elif MODE==MODE_TWO_LEGS:
    MODE_NAME = "two_legs"
    # Use these settings for two-legged operation
    #          Left                  Right
    #          Hip        Knee       Hip        Knee
    #          F   B      U    D     F    B     U   D      = Forward, Backward, Up, Down
    SERVOS = [[45, 135], [130, 80], [135, 45], [50, 100]]
    SERVO_PIN_START = 2

elif MODE==MODE_FOUR_SIMPLE_LEGS:
    MODE_NAME = "four_simple_legs"
    # Use these settings for 4-legged operation
    #SERVOS = [[90,50], [90,130], [90,50], [90,130]]
    #SERVOS = [[130,50], [50,130], [130,50], [50,130]]
    SERVOS = [[110,70], [70,130], [110,70], [70,110]]
    SERVO_PIN_START = 2

# Use these settings for 4-legged + weight operation
#SERVOS = [[130,50], [50,130], [130,50], [50,130], [20, 160]]
#SERVO_PIN_START = 2

# Whether to always choose the best option or to have some randomness
#MOVE_CHOICE = "best"
#MOVE_CHOICE = "q"
MOVE_CHOICE = "geom"


DATA_DIR = 'data_' + str(MODE_NAME)
MOVEMENTS_FILENAME = DATA_DIR + '/movements.csv'
R_FILENAME = DATA_DIR + '/r.npy'
C_FILENAME = DATA_DIR + '/c.npy'
Q_FILENAME = DATA_DIR + '/q.npy'

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

# Number of episodes to run when learning Q
LEARN_Q_EPISODES = 2000

# Maximum movement that we will register (in cm) when learning R
# If more than this then we must have an error (e.g. ultrasonic sensor misreading)
LEARN_R_MAX_RECORDED_MOVE = 20

# Number of seconds to wait between movements
RECORD_WAIT_BETWEEN_MOVES = 1

# Number of seconds to wait between movements
MOVE_Q_WAIT_BETWEEN_MOVES = 1