import digits
import clocks
import time
from machine import Pin

laneSensors = []
laneSensors.append(Pin(18, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(19, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(20, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(21, Pin.IN, Pin.PULL_DOWN))

startSwitch = Pin(4, Pin.IN, Pin.PULL_DOWN)

# Show "LINE UP" on the displays
def displayWaiting():
    clocks.showUP()
    digits.showLINE()
#end displayWaiting()

# When starting switch is pressed, blank all times & screens
def gateIsClosed():
    return startSwitch.value()
#end gateIsOpen()

def waitForStart():
    while gateIsClosed():
        time.sleep(0.001)
    return
#end waitForStart()

def laneFinished(lane):
    # Our sensor sends HI/True in the dark, and LO/False when illuminated.
    # A dark lane means a car is blocking the laser - ie: Finished
    return laneSensors[lane].value()
#end laneFinished()

def watchForFinishers(start):
    # Wipe the "LINE UP" message
    digits.blankAll()
    clocks.blankAll()
    # A lane is 'active' if it hasn't yet finished
    activeLanes = [0,1,2,3]
    leaderboard = []
    finishTimes = [None,None,None,None]
    while True:
        # If they close the gate, reset for next race:
        if gateIsClosed():
            return
        #end if
        
        # Gate's still open, so potentially cars are still racing
        changed = False
        for lane in activeLanes:
            if laneFinished(lane):
                # If so, add to leaderboard and record finishing time
                leaderboard.append(lane)
                #finishTimes[lane] = time.ticks_ms()
                finishTimes[lane] = time.ticks_diff(time.ticks_ms(),start)
                # Lane has finished, so is no longer 'active'
                activeLanes.remove(lane)
                changed = True
            #end if
        # end for
        if changed:
            # Update displays, gold-first
            for rank in range(len(leaderboard)):
                lane = leaderboard[rank]
                digits.showX(rank+1,lane)
                clocks.showTimeOnX(finishTimes[lane],lane)
            #end for
        #end if
        # Wait 1/10th of a scorable time unit:
        time.sleep(0.001)
    #end while
#end watchForFinishers()


def REPL():
    while True:
        # Display "LINE UP"
        displayWaiting()
        # Wait for gate to open
        waitForStart()
        # Gate opened, cars must be racing.
        watchForFinishers(time.ticks_ms())
    #end while
#end REPL()
        
REPL()


