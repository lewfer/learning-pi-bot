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
        sleep(1)
        bot.moveTo('02')
        sleep(1)
        bot.moveTo('12')
        sleep(1)
        bot.moveTo('10')
        sleep(1)

elif len(SERVOS)==4:    # Make pre-determined movements
    delay = 0.2
    for i in range(10):
        #FL-FR-BL-BR
        '''
        bot.moveTo('0101')
        sleep(1)
        bot.moveTo('1111')
        sleep(1)
        bot.moveTo('1010')
        sleep(1)
        bot.moveTo('0000')
        sleep(1)
        '''
    
        '''
        bot.moveTo('0101')
        sleep(delay)
        bot.moveTo('1010')
        sleep(delay)
        '''

        bot.moveTo('0110')
        sleep(delay)
        bot.moveTo('1001')
        sleep(delay)

elif len(SERVOS)==5:    # Make pre-determined movements
    delay = 1
    for i in range(10):
        #FL-FR-BL-BR-WEIGHT      
        bot.moveTo('00001') # right legs back, left legs forward
        sleep(delay)   
        bot.moveTo('10101') # right legs back, left legs forward
        sleep(delay)  
        bot.moveTo('10100') # swing left
        sleep(delay)
        bot.moveTo('00000') # left legs back, right legs forward
        sleep(delay)
        bot.moveTo('01010') # left legs back, right legs forward
        sleep(delay)
        bot.moveTo('01011') # swing right
        sleep(delay)
