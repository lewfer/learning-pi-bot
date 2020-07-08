# Learnbot Cheat
#
# Move the robot based on human-selected behaviours
# 

from learnbot import *
from time import sleep

# Create the bot
bot = Learnbot(SERVOS)

# Start it up
bot.wakeSlowly(2) 

if len(SERVOS)==2:
    # Make pre-determined movements
    for i in range(10):
        bot.moveTo('00')
        bot.moveTo('02')
        bot.moveTo('12')
        bot.moveTo('10')

elif len(SERVOS)==4:    # Make pre-determined movements
    for i in range(10):
        #FL-FR-BL-BR
        bot.moveTo('0001')
        sleep(0.2)
        bot.moveTo('0000')
        sleep(0.2)
        bot.moveTo('1000')
        sleep(0.2)
        bot.moveTo('1001')
        sleep(0.2)
