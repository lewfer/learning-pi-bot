# Learnbot Cheat
#
# Move the robot based on human-selected behaviours
# 

from learnbot import *

# Create the bot
bot = Learnbot([[170, 90], [135, 90, 0]])

# Start it up
bot.wakeSlowly(2) 

# Make pre-determined movements
for i in range(10):
    bot.moveTo('00')
    bot.moveTo('02')
    bot.moveTo('12')
    bot.moveTo('10')