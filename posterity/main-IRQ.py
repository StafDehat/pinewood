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

startTime = None
finishTimes = [None,None,None,None]
leaderboard = []
numDisplayed = 0 

def startSwitchCallback(pin):
    flags = pin.irq().flags()
    now = time.ticks_ms()
    global startTime
    global numDisplayed
    # Check to see if interrupt is rising or falling edge. Rising is the gate opening. Falling is it closing.
    #if(startTime is None and (flags & Pin.IRQ_RISING)):
    if (flags & Pin.IRQ_RISING):
        #print("Gate opened, race starting");
        startTime=now
        numDisplayed=0
    else:
    #elif(flags & Pin.IRQ_FALLING):
        #print("Gate closed, LINE UP");
        startTime=None
        for x in range(len(finishTimes)):
            finishTimes[x] = None
        leaderboard.clear()
startSwitch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=startSwitchCallback)

def laneCallback(pin):
    now = time.ticks_ms()
    # Get the index of the pin that fired interrupt. This will be the same as the lane index.
    index = laneSensors.index(pin)
    global finishTimes
    global leaderboard
    # Make sure race is started and only the first finished time is stored. 
    if((finishTimes[index] is None) & (startTime is not None)):
        finishTimes[index]=time.ticks_diff(now,startTime)
        leaderboard.append(index)

for lane in laneSensors:
    lane.irq(trigger=Pin.IRQ_RISING, handler=laneCallback)

# Show "LINE UP" on the displays
def displayWaiting():
    clocks.showUP()
    digits.showLINE()
#end displayWaiting()

def waitForStart():
    # Loop forever here until IRQ starts the race by setting the startTime
    while(startTime is None):
        pass
#end waitForStart()

def watchForFinishers(): 
    global numDisplayed
    global leaderboard
    # Wipe the "LINE UP" message
    digits.blankAll()
    clocks.blankAll()
    while startTime is not None:
        # If they close the gate, reset for next race:
        # Gate's still open, so potentially cars are still racing
        if len(leaderboard) > numDisplayed:
            # Update displays, gold-first
            for rank in range(len(leaderboard)):
                lane = leaderboard[rank]
                digits.showX(rank+1,lane)
                clocks.showTimeOnX(finishTimes[lane],lane)
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
        watchForFinishers()
    #end while
#end REPL()

REPL()

