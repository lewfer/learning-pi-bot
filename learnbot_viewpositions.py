# Learnbot View Positions
#
# Run the robot though each position in turn, just so we can see them

from learnbot import *

from settings import *

#indices=['00','01','02','10','11','12']


# Create the bot
bot = Learnbot(SERVOS)

# Start it up
bot.wakeSlowly(2) 

# View all the positions in order
for state in bot.state_codes:
    bot.moveTo(state)
    print("Position", state)
    sleep(5)