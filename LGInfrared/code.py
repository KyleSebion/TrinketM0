import board
import pwmio
import pulseio
import array
import touchio
import time
import adafruit_dotstar

#based on https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol
#   and timing measurements on universal remote
preamble = [9000, 4500]
period1 = 560
period2 = period1 * 3
b0 = [period1, period1]
b1 = [period1, period2]
end = [period1]
bits = { '0': b0, '1': b1 }
inv = { '0': '1', '1': '0' }

def getBinWithInv(byteVal):
    byteValB = '{0:08b}'.format(byteVal)
    return list(byteValB) + [ inv[c] for c in byteValB ]

def getPulseArray(valB):
    return array.array('H', preamble + list([ p for c in valB for p in bits[c] ]) + end)

def getPulses(byteAddr, byteCmd):
    addrB = getBinWithInv(byteAddr)
    cmdB = getBinWithInv(byteCmd)
    return getPulseArray(addrB + cmdB)

def getPulsesUInt32(val):
    valB = '{0:032b}'.format(val)
    return getPulseArray(valB)

#codes https://gitlab.com/snippets/1690600
#all of the following are the same
#onoffPulses = array.array('H', preamble + b0+b0+b1+b0 + b0+b0+b0+b0 + b1+b1+b0+b1 + b1+b1+b1+b1 + b0+b0+b0+b1 + b0+b0+b0+b0 + b1+b1+b1+b0 + b1+b1+b1+b1 + end)
#onoffPulses = getPulsesUInt32(0x20DF10EF)
#onoffPulses = getPulses(0x20,0x10)

p = pwmio.PWMOut(board.A1, frequency=38000, duty_cycle=0x8000)
b = pulseio.PulseOut(p)

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dotOff = [0,0,0]
dot[0] = dotOff

btnMap = [
    { 'desc': 'off',    'pulses': getPulses(0x20, 0xA3), 'btn': touchio.TouchIn(board.A4), 'dotVal': [255,  0,  0] },
    { 'desc': 'on',     'pulses': getPulses(0x20, 0x23), 'btn': touchio.TouchIn(board.A3), 'dotVal': [  0,255,  0] },
    { 'desc': 'onoff',  'pulses': getPulses(0x20, 0x10), 'btn': touchio.TouchIn(board.A0), 'dotVal': [255,255,  0] }
]

while True:
    input = None
    for btnItem in btnMap:
        if btnItem['btn'].value:
            input = btnItem
    if input:
        dot[0] = input['dotVal']
        b.send(input['pulses'])
        time.sleep(0.5)
        dot[0] = dotOff
    time.sleep(0.01)
