# Learnbot View Positions
#
# Run the robot though each position in turn, just so we can see them

from learnbot import *

indices=['00','01','02','10','11','12']


# Create the bot
bot = Learnbot()

# Start it up
bot.wakeSlowly(2) 

# View all the positions in order
for index in indices:
    print("Position", index)
    bot.moveTo(index)
    sleep(3)