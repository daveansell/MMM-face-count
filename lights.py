import time
import board
import neopixel
import os
import sys

pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 28

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


while True:
    ch = os.read(sys.stdin.fileno(), 1)
    print (ch) 
    if ch==b'1':
        print ("on")
        pixels.fill((255, 255, 255))
        os.system("./ledsOn")
    elif ch==b'0':
        pixels.fill((0,0,0))
        os.system("./ledsOff")
    elif ch==b'q':
        sys.exit()
    pixels.show()

