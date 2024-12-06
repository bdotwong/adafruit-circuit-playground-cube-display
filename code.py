# SPDX-FileCopyrightText: 2018 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Jack-o'-Lantern flame example with toggle functionality"""

import math
import board
import neopixel
import digitalio
import time
try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random

# LED and Button Setup
NUMPIX = 10        # Number of NeoPixels
PIXPIN = board.D8  # Pin where NeoPixels are connected
STRIP = neopixel.NeoPixel(PIXPIN, NUMPIX, brightness=0.5)

button = digitalio.DigitalInOut(board.D4)
button.switch_to_input(pull=digitalio.Pull.DOWN)

PREV = 128

# State variables
mode = 0  # 0 = Flame mode, 1 = Static white, 2 = Blinking
last_button_state = False  # To track button presses

def split(first, second, offset):
    """
    Subdivide a brightness range, introducing a random offset in middle,
    then call recursively with smaller offsets along the way.
    @param1 first:  Initial brightness value.
    @param1 second: Ending brightness value.
    @param1 offset: Midpoint offset range is +/- this amount max.
    """
    if offset != 0:
        mid = ((first + second + 1) / 2 + random.randint(-offset, offset))
        offset = int(offset / 2)
        split(first, mid, offset)
        split(mid, second, offset)
    else:
        level = math.pow(first / 255.0, 2.7) * 255.0 + 0.5
        STRIP.fill((int(level), int(level / 8), int(level / 48)))
        STRIP.write()

def static_white():
    """Turn all LEDs solid white."""
    STRIP.fill((255, 255, 255))
    STRIP.write()

def blink():
    """Blink all LEDs in sequence."""
    for i in range(NUMPIX):
        STRIP[i] = (255, 255, 255)  # Turn on one LED
        STRIP.write()
        time.sleep(0.1)  # Delay
        STRIP[i] = (0, 0, 0)  # Turn off the LED
        STRIP.write()

while True:  # Main loop
    button_state = button.value  # Check if the button is pressed

    # Check for button press (rising edge)
    if button_state and not last_button_state:
        mode = (mode + 1) % 3  # Cycle between 0, 1, and 2
        time.sleep(0.2)  # Debounce delay

    last_button_state = button_state  # Save button state

    # Execute behavior based on mode
    if mode == 0:  # Flame effect
        LVL = random.randint(64, 191)
        split(PREV, LVL, 32)
        PREV = LVL

    elif mode == 1:  # Solid white
        static_white()

    elif mode == 2:  # Blinking LEDs in sequence
        blink()
