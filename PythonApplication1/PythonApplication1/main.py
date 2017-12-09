import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import touchio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar
import time
import neopixel

dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

td1 = touchio.TouchIn(board.D1)
td3 = touchio.TouchIn(board.D3)
td4 = touchio.TouchIn(board.D4)
kbd = Keyboard()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos * 3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos * 3), 0, int(pos * 3)]
    else:
        pos -= 170
        return [0, int(pos * 3), int(255 - pos * 3)]

i = 0
while True:
  setLed = td1.value | td3.value | td4.value
  led.value = setLed
  colors = None
  if setLed:
    colors = [td1.value * 128, td4.value * 128, td3.value * 128]
  else:
    colors = wheel(i & 255)
    i = (i + 1) % 256
  print(colors)
  dot[0] = colors

  #kbd.press(Keycode.A)
  #kbd.release_all()

  time.sleep(0.01)
