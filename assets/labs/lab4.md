---
layout: page
title: Lab 4
nav_exclude: True
description: >-
    Lab 4 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 4 - Sensors

We have learned how to interact with our devices in terms of button presses and LEDs, now it is time to use them as they might be deployed in the field - reading data.

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

1. The temperature sensor in use (reading/printing values).

2. The light sensor in use (reading/printing values).

## Make your backup

Don't forget!

## Getting started

Some boilerplate code for you to get up and running:

```
from time import sleep
import board
import neopixel
import gc
import digitalio
import touchio

# initialize neopixels
NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, brightness=0.15,auto_write=False)

# named colors
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# set pixels to off initially
for i in range(NUM_LEDS):
    pixels[i] = OFF
pixels.show()

# setup buttons
btnA = digitalio.DigitalInOut(board.BUTTON_A)
btnA.switch_to_input(pull=digitalio.Pull.DOWN)

btnB = digitalio.DigitalInOut(board.BUTTON_B)
btnB.switch_to_input(pull=digitalio.Pull.DOWN)
BTN_TIMER_DELAY = 15
btn_timer = 0

# capacitive touch
touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)

done = False
while not done:
    if btnA.value and btnB.value: # Both buttons pressed - exit
        done = True
    else:
        if btnA.value and btn_timer == 0:
            btn_timer = BTN_TIMER_DELAY

        if btnB.value and btn_timer == 0:
            btn_timer = BTN_TIMER_DELAY

    # A1 side
    if touch_A1.value or touch_A2.value or touch_A3.value:
        pass

    # A4 side
    if touch_A4.value or touch_A5.value or touch_A6.value or touch_TX.value:
        pass

    # Handle button cooldown
    if btn_timer > 0: btn_timer -= 1    

    pixels.show()
    sleep(.1)
    gc.collect()

print("Program done - exiting.")

```

## Reading temperature 

Sensor motes typically need to record information, so let's start out with temperature!

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/054/798/medium800/circuitpython_cpx_temperature.jpg?1527980477" alt="temp sensor" />
</div>

We're going to need the `adafruit_thermistor.mpy` library from the [community bundle](https://github.com/adafruit/CircuitPython_Community_Bundle/releases/download/20240116/circuitpython-community-bundle-8.x-mpy-20240116.zip).  (You most likely still have this in your Downloads folder on your computer.)  Copy it into the `lib` directory on your device.

Then, in your imports:

`import adafruit_thermistor`

and in your globals:

```
# setup sensors
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
```

and in your forever loop (outside of the button presses):

```
temp_c = thermistor.temperature
temp_f = thermistor.temperature * 9 / 5 + 32
print("Temperature is: %f C and %f F" % (temp_c, temp_f))
```

This should print out the current temperature.  You might notice it fluctuate as it is reading every loop and the sensor has a reasonable amount of precision.  

We're going to record our "resting" temperature to see what the baseline is without touching anything.

{: .note }
The temperature being recorded is being impacted by the device itself!  This holds true for any device - typically to get a "true" reading of the temperature you need to either move the temperature sensor off of the device or calculate the ambient temperature of the room and figure out what the difference is!

Comment out the print statement in the forever loop - we don't want it to obliterate our next calls.

The following code "samples" the temperatures over a small period of time and then calculates the average within `resting_temp`.  We'll use that as our baseline later.

```
# Sample resting temperature when program starts to get baseline
print("Calculating resting temperature...")
resting_temps = []
for i in range(20):
    resting_temps.append(thermistor.temperature)
    sleep(0.5)
resting_temp = sum(resting_temps) / len(resting_temps)
print("Resting temperature is {0}C".format(resting_temp))
```

Now, we're going to do the same thing with our maximum temperature.  Since we don't have any heat sources here, you'll have to use your finger.  We're going to copy the prior code and modify it slightly. 

However, there is just one issue - we need to know when to start!  The simplest way will be to add a delay once it is done (we could handle on a button press, but then we get into state machines and it gets a bit much for this lab).

So, after your measurement of the resting temperature, give yourself a five second warning:

```
# Calculate what our maximum temperature will be
print("Put your finger on the temperature sensor")
sleep(5)

max_temps = []
for i in range(20):
    max_temps.append(thermistor.temperature)
    sleep(0.5)
max_temp = sum(max_temps) / len(max_temps)
print("Maximum temperature is {0}C".format(max_temp))
sleep(1)
```

We now have captured the (relative) minimum and maximum values that we'll be reading.  This is important as we need to know what boundaries our sensors will typically be experiencing.

Let's now test out our readings.  First, a slight diversion into normalization...

## Normalization

We're now going to do something called *normalizing* data.  While there are many definitions, we're going to consider the simplified version of taking one range of values and mapping it to another range.  

What we will do to test things out is to map the pixel brightness to your temperature reading.  The "resting" value will be 0.0 and the "maximum" value will be 1.0.

Here is a function for mapping ranges (c/o the p5js library - I use this all the time for mapping values to other ranges):

```
def p5map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2
```

{: .note }
There is a CircuitPython library that provides a similar feature - `simpleio`.  However, for a basic function we don't need to add and import yet another library...

This function will return a value mapped to the range you want it to be in.  For example, if I had a variable named `current_value` that exists between 25.0 and 28.0 and I want to map it to a range of 0.0 to 1.0, then I would call it as:

```
# current_value is somewhere between 25.0 and 28.0, and we want to map it to a range of 0.0 to 1.0
mapped_value = p5map(current_value, 25.0, 28.0, 0.0, 1.0) 
```

For example, if `current_value = 27.5`, then `mapped_value` would be returned as `0.83` (truncated).

{: .warning }
The `p5map` function as is does not constrain your values to the specified range!  If you send in a lower or higher value then it will try to map.  For instance, if you send in `20.0` to the above function it will return `-1.67`.  Meaning, **you** need to test for its return value to make sure it is within bounds!

### Mapping to brightness

Let's now map our temperature reading to brightness.  We have a reasonable check on temperature.

In your forever loop, above the call to `pixels.show()`:

```
current_temp = thermistor.temperature
print("Current temp [{0}], Resting temp [{1}], Max temp [{2}]".format(current_temp, resting_temp, max_temp))
```

You should be seeing a printout of the various temperature values.

Now, let's go ahead and turn on the lights:

{: .note }
Before we individually set the pixel values to understand how to access each individual pixel.  The call to `pixels.fill` will set *all* LEDs at once.

```
pixels.fill(RED)
```

Time for the magic to happen.  Let's get our mapped value **and** constrain it to the correct range.

{: .note }
You could do this with a `min`-`max` one-liner, however this is a bit more readable for the time being.

Above your print statement in your forever loop:

```
mapped_value = p5map(current_temp, resting_temp, max_temp, 0.0, 1.0)
if mapped_value < 0.0: mapped_value = 0.0
if mapped_value > 1.0: mapped_value = 1.0
```

And update your print statement (this is just for debugging):

```
print("Current temp [{0}], Resting temp [{1}], Max temp [{2}], Mapped value [{3}]".format(current_temp, resting_temp, max_temp, mapped_value))
```

Now, let's finish this piece up.  Right before you set the LED colors:

`pixels.brightness = mapped_value`

{: .note }
You may notice something odd - if you follow straight through does the resting temperature ever get back to where it was?  What happens if you turn on the LEDs **before** you calculate the resting temperature?

## Reading light

We are essentially going to do the same thing, calculate the resting and max values (just in reverse).

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/054/795/medium800/circuitpython_cpx_light_sensor.jpg?1527979530" alt="light sensor" />
</div>

First, a new import:

`import analogio`

And a new global object:

```
light = analogio.AnalogIn(board.LIGHT)
resting_lights = []
print("Calculating resting light...")
resting_lights = []
for i in range(20):
    resting_lights.append(light.value)
    sleep(0.5)
resting_light = sum(resting_lights) / len(resting_lights)

print("Resting light value is {0}".format(resting_light))
```

Rather than calculate the maximum, we're going to calculate the minimum (as you're going to be covering up the light sensor with your hand).  Same process - give yourself a five-second delay to get setup and then cover the light sensor with your hand to block as much light as possible.

```
print("Cover up the light sensor")
sleep(5)

min_lights = []
for i in range(20):
    min_lights.append(light.value)
    sleep(0.5)
min_light = sum(min_lights) / len(min_lights)
print("Minimum light value is {0}".format(min_light))
sleep(1)
```
---

### Sensor interactions 

This brings up an interesting conflict.  Let's explore.

In our forever loop, print the light value:

`print(light.value)`

If you are doing nothing to the sensor (and have been following the lab in order), does the values you are seeing in the serial console make sense?  Shouldn't it be the same as our resting light value?  

{: .note }
If the above doesn't make sense - make sure you got the LED aspect of the temperature sensor working...

What happens if you cover up the light sensor?  Does it go to the minimum value?

## Back to the light

Now, comment out the calls to `mapped_value` for the thermometer (save them - you'll use them soon).

Replace them with:

```
mapped_value = p5map(light.value, min_light, resting_light, 0, .15)
if mapped_value < 0.0: mapped_value = 0.0
if mapped_value > 1.0: mapped_value = 1.0
pixels.brightness = mapped_value
```

{: .warning }
Unless if you want to blind yourself, I don't recommend going full brightness here.

Your LEDs should now correspond to the lightness.  

{: .note }
When testing (covering up the light sensor) I'd recommend covering it with a piece of clothing, like a shirt sleeve.  It seems to work better than a finger.

## Homework - Mapping to LEDs (Part 1 of 2)

We'll be logging data soon.  For now, we have two options for sending information to users - via serial (not user-friendly) or LEDs (user-friendly).  We'll choose the latter for your homework.

---

**Note - there is no code deliverable for this one as you'll be completing Part 2 next week - you still have questions to answer in Blackboard though!**

---

Your assignment is to show the relative temperature and relative light, in color, on the LEDs.  The brightness should be made constant now.

{: .warning }
You may have noticed that there are significant interactions between our sensors - therefore we are going to have them work **separately**.

Here is a short overview of what should happen:

* By default (i.e., when the device is powered on), the LEDs should react to the temperature sensor and output red.

* When you press either of the buttons (A or B), toggle the behavior to have the LEDs react to the light sensor and output green.

    * This means that you need a flag to show whether the temperature or light sensor is being used - hitting a button will update that flag.

    * If you hit a button again, it should go back to using temperature.

* Recall that colors are tuples of 3 integer values - `(R, G, B)`

    * When a sensor value is at or below its resting state, output a value of 0 to the pixel array.
    * When a sensor value is at or above its maximum state, output a value of 255 to the pixel array in the correct color (i.e., if temperature, map to red; if light, map to green).
    * When a sensor value is in between resting and maximum, output a mapped value between (0, 255) to the corresponding pixels in the correct color.

---

For example, it should look like this:


Q's:

It's very jittery - why and how to fix?
What happens if you don't record max temp?
What happens if you cover up the

# References

* [Temperature sensor](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/temperature)
* [Light sensor](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/light)