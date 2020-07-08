# readkeys
# 
# Functions to read keys from the keyboard

from threading import Thread
from time import sleep
import sys, tty, termios

# Stores the last key read
last_key = None

def getch():
    '''Read a single key from the keyboard'''

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        #tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getKeys(break_ch):
    '''Read keys until the break key is read'''

    global last_key
    while True:
        ch = getch()
        last_key = ch
        if ch==break_ch:
            break

def startCheckKeys():
    '''Start a thread to read keys in the background.  Use this so that we don't block'''

    thread = Thread(target=getKeys, kwargs={"break_ch":" "})
    thread.start()


# Test code
if __name__ == "__main__":
    startCheckKeys()
    while last_key!=" ":
        print(last_key)
        sleep(1)

