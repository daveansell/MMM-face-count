import time
import board
import neopixel
import os
import sys

# Turns on and off a strip of neopixels, and the Pi's leds

pixel_pin = board.D18
directory = os.path.dirname(os.path.realpath(__file__))
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
        os.system(directory+"/ledsOn")
    elif ch==b'0':
        pixels.fill((0,0,0))
        os.system(directory+"/ledsOff")
    elif ch==b'q':
        sys.exit()
    pixels.show()

