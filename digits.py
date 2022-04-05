import max7219
from machine import Pin, SPI

DIN = 3 # SPI0_TX
CS  = 5 # SPI0 CSn
CLK = 2 # SPI0 SCK
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(CLK), mosi=Pin(DIN))
ss = Pin(CS, Pin.OUT)

display = max7219.Matrix8x8(spi, ss, 4)
display.brightness(1) #1-15
display.fill(0)
display.show()

def showX(digit, pos):
    print("Displaying digit %d in lane %d" % (digit, pos))
    if digit == 1:
        show1(pos)
    elif digit == 2:
        show2(pos)
    elif digit == 3:
        show3(pos)
    elif digit == 4:
        show4(pos)
#end showX()
    
def show1(pos):
    xOffset = (pos)*8
    display.fill_rect(xOffset,0,8,8,0)
    display.fill_rect(xOffset+3,0,2,8,1)
    display.pixel(xOffset+2,1,1)
    display.hline(xOffset+2,7,4,1)
    display.show()

def show2(pos):
    xOffset = (pos)*8
    display.fill_rect(xOffset,0,8,8,0)
    display.hline(xOffset+2,0,4,1)
    display.fill_rect(xOffset+1,1,2,2,1)
    display.pixel(xOffset+5,1,1)
    display.line(xOffset+1,6,xOffset+6,1,1)
    display.line(xOffset+1,7,xOffset+6,2,1)
    display.hline(xOffset+1,7,6,1)
    display.show()

def show3(pos):
    xOffset = (pos)*8
    display.fill_rect(xOffset,0,8,8,0)
    display.hline(xOffset+1,0,6,1)
    display.line(xOffset+6,0,xOffset+3,3,1)
    display.line(xOffset+6,1,xOffset+4,3,1)
    display.fill_rect(xOffset+5,4,2,3,1)
    display.hline(xOffset+1,6,2,1)
    display.hline(xOffset+2,7,4,1)
    display.show()


def show4(pos):
    xOffset = (pos)*8
    display.fill_rect(xOffset,0,8,8,0)
    display.vline(xOffset+1,1,4,1)
    display.vline(xOffset+2,0,5,1)
    display.fill_rect(xOffset+4,0,2,8,1)
    display.hline(xOffset+1,4,6,1)
    display.hline(xOffset+3,7,4,1)
    display.show()

def blankAll():
    display.fill(0)
    display.show()

def underline():
    blankAll()
    for x in range(4):
        display.line(x*8+1,7,x*8+6,7,1)
    display.show()
#end underline()

def showLINE():
    blankAll()
    # L
    display.fill_rect(1,0,2,8,1)
    display.fill_rect(1,6,6,2,1)
    # I
    display.fill_rect(11,0,2,8,1)
    # N
    display.fill_rect(17,0,2,8,1)
    display.vline(19,1,4,1)
    display.vline(20,3,4,1)
    display.fill_rect(21,0,2,8,1)
    # E
    display.fill_rect(25,0,2,8,1)
    display.fill_rect(25,0,6,2,1)
    display.fill_rect(25,3,4,2,1)
    display.fill_rect(25,6,6,2,1)
    display.show()
#end showLINE()

underline()
