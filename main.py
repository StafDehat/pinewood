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

startTime = None
finishTimes = [None,None,None,None]
leaderboard = []
refreshDisplay = False

def startSwitchCallback(pin):
    flags = pin.irq().flags()
    now = time.ticks_us()
    global startTime
    # Check to see if interrupt is rising or falling edge. Rising edge will start race. Falling edge resets it.
    if(startTime is None and (flags & Pin.IRQ_RISING)):
        startTime=now
    elif(flags & Pin.IRQ_FALLING):
        startTime=None
        print("Gate Closed")
        for x in range(len(finishTimes)):
            finishTimes[x] = None
        leaderboard.clear()

startSwitch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=startSwitchCallback)

def laneCallback(pin):
    now = time.ticks_us()
    # Get the index of the pin that fired interrupt. This will be the same as the lane index.
    index = laneSensors.index(pin)
    global finishTimes
    global leaderboard
    global refreshDisplay
    # Make sure race is started and only the first finished time is stored. 
    if((finishTimes[index] is None) & (startTime is not None)):
        finishTimes[index]=now-startTime
        leaderboard.append(index)
        refreshDisplay = True

for lane in laneSensors:
    lane.irq(trigger=Pin.IRQ_FALLING, handler=laneCallback)

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
    global refreshDisplay
    # Wipe the "LINE UP" message
    digits.blankAll()
    clocks.blankAll()   
    while startTime is not None:
        # If they close the gate, reset for next race:
        # Gate's still open, so potentially cars are still racing
        if refreshDisplay:
            # Update displays, gold-first
            for rank in range(len(leaderboard)):
                lane = leaderboard[rank]
                digits.showX(rank+1,lane)
                clocks.showTimeOnX(finishTimes[lane],lane)
            #end for
            refreshDisplay = False
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
        watchForFinishers()
    #end while
#end REPL()

REPL()