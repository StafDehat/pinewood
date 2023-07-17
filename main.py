import digits
import clocks
import time
from machine import Pin

laneSensors = []
laneSensors.append(Pin(18, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(19, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(20, Pin.IN, Pin.PULL_DOWN))
laneSensors.append(Pin(21, Pin.IN, Pin.PULL_DOWN))

startSwitch = Pin(4, Pin.IN, Pin.PULL_UP)

finishTimes = [None,None,None,None]
leaderboard = []

# Use IRQ to detect finishers, for maximum granularity.
def laneCallback(pin):
    now = time.ticks_ms()
    global finishTimes
    global leaderboard
    # Get the index of the pin that fired interrupt. This will be the same as the lane index.
    index = laneSensors.index(pin)
    # Only record the first time this beam gets broken
    if(finishTimes[index] is not None):
        return
    #end if
    finishTimes[index]=now
    leaderboard.append(index)
#End laneCallback()
# Apply laneCallback() to each lane's laser-sensor IRQ:
for lane in laneSensors:
    lane.irq(trigger=Pin.IRQ_RISING, handler=laneCallback)
#end for

# Show "LINE UP" on the displays
def displayWaiting():
    clocks.showUP()
    digits.showLINE()
#end displayWaiting()

# When starting switch is pressed, blank all times & screens
def gateIsClosed():
    return not startSwitch.value()
#end gateIsOpen()

def waitForStart():
    while gateIsClosed():
        time.sleep(0.001)
    return
#end waitForStart()

def watchForFinishers(startTime):
    global leaderboard
    # Wipe record of previous race:
    leaderboard.clear()
    for x in range(len(finishTimes)):
        finishTimes[x] = None
    numDisplayed = 0
    # Wipe the "LINE UP" message
    digits.blankAll()
    clocks.blankAll()
    while True:
        # If they close the gate, reset for next race:
        if gateIsClosed():
            return
        #end if
        # Gate's still open, so potentially cars are still racing
        if len(leaderboard) > numDisplayed:
            # Update displays, gold-first
            for rank in range(len(leaderboard)):
                lane = leaderboard[rank]
                lapTime = time.ticks_diff(finishTimes[lane], startTime)
                digits.showX(rank+1,lane)
                clocks.showTimeOnX(lapTime, lane)
            #end for
            numDisplayed += 1;
        #end if
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

