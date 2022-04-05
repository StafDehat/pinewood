import tm1637
from machine import Pin

BRIGHTNESS = 5

clocks = []
clocks.append(tm1637.TM1637(Pin(6),Pin(7),BRIGHTNESS))
clocks.append(tm1637.TM1637(Pin(8),Pin(9),BRIGHTNESS))
clocks.append(tm1637.TM1637(Pin(10),Pin(11),BRIGHTNESS))
clocks.append(tm1637.TM1637(Pin(12),Pin(13),BRIGHTNESS))

def showUP():
    #[ clock.write([0x00,0x3E,0x73,0x00]) for clock in clocks ]
    [ clock.show(" UP ") for clock in clocks ]
#end showUp()

def showTimeOnX(ms, pos):
    if ms <= 99999:
        clocks[pos].showMs(ms)
        return
    clocks[pos].show("DNF ")
#end showX()

def blankAll():
    [ clock.show("    ") for clock in clocks ]
#end blankAll()

def underline():
    [ clock.write([0x08,0x08,0x08,0x08]) for clock in clocks ]
#end underline()

blankAll()
underline()
