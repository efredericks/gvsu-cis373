---
layout: page
title: Lab 9
nav_exclude: True
description: >-
    Lab 9 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 9 - Accelerometer and Visualizations!

In this lab we're going to transmit sensor data (specifically the accelerometer) to a webpage that has Bluetooth enabled.  

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Your device printing accelerometer data to the terminal **to the same place**.

## Make your backup

We're going to be "starting fresh" and then merging our two scripts.  So, backup last week's code and create a new `code.py` file.

## Getting started

Ensure you have the `adafruit_circuitplayground` library installed (should be a folder copy from our downloaded library bundle).  I'm sure there's a nice way to read the data via the `board` object, however for simplicity in this lab we're going to go with the "other" device library.  

{: .warning}
This will significantly mess with anything related to the neopixels, so if you have designs on including them you'll need to translate your code to the `adafruit_circuitplayground` style of interacting with them!  See [Adafruit - NeoPixels](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/neopixels) for more information.

## First, the accelerometer

We played with this a bit in the last lab without much explanation.  Your devices have an accelerometer built in that we can access pretty easily.

![accelerometer](https://cdn-learn.adafruit.com/assets/assets/000/086/567/large1024/circuitpython_Circuit_Playground_Bluefruit_Accelerometer.jpeg?1577994382)

Essentially, it measures acceleration on all axes (x, y, and z), including gravity (read more up on acceleration [here](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration)). 

If your device is lying flat, it should read `(0, 0, 9.8)` for acceleration, though it will probably not quite be that perfect.  For instance, my board using the demo code (below) looks like this.  

<div align="center">
  <img src="/gvsu-cis373/assets/images/acceleration_flat.png" alt="Accelerometer Bluetooth connection to UART" />
</div>

{: .highlight }
What is the 9.8 value?

Here's the demo code from the acceleration link above:

```
"""
This example uses the accelerometer on the Circuit Playground. It prints the values. Try moving
the board to see the values change. If you're using Mu, open the plotter to see the values plotted.
"""
import time
from adafruit_circuitplayground import cp

while True:
    x, y, z = cp.acceleration
    print((x, y, z))

    time.sleep(0.1)
```

Interestingly, the plotter works for this code as well.  Open the Plotter in Mu and check out the values being drawn!

{: .note }
Wondering about the plotter and how to use it?  Check out [this link](https://codewith.mu/en/tutorials/1.0/plotter).  The tl;dr is you need to be printing a tuple of information for it to work.

Now, try moving your device around and getting a feeling for the different values.  One way you can do that is to *isolate* an axis to rotate around.  For instance, only make one rotational or translational motion on an axis to see things happen.

![axes](https://i.stack.imgur.com/FS7OG.png)


### Get them working with LEDs

This code is also from Adafruit, but now your LEDs are working with your accelerometer.  I'm including this verbatim because we now have to interact with our LEDs using the `adafruit_circuitplayground` library, rather than the `board` library we're used to.  I did modify it *slightly* to include a delay, otherwise Mu tends to freeze up.

Interestingly, the example also includes example code for working with the slide switch!

```python
"""If the switch is to the right, it will appear that nothing is happening. Move the switch to the
left to see the NeoPixels light up in colors related to the accelerometer! The Circuit Playground
has an accelerometer in the center that returns (x, y, z) acceleration values. This program uses
those values to light up the NeoPixels based on those acceleration values."""

from adafruit_circuitplayground import cp
import time

# Main loop gets x, y and z axis acceleration, prints the values, and turns on
# red, green and blue, at levels related to the x, y and z values.
while True:
    if not cp.switch:
        # If the switch is to the right, it returns False!
        print("Slide switch off!")
        cp.pixels.fill((0, 0, 0))
        continue
    R = 0
    G = 0
    B = 0
    x, y, z = cp.acceleration
    print((x, y, z))
    cp.pixels.fill(((R + abs(int(x))), (G + abs(int(y))), (B + abs(int(z)))))

    time.sleep(0.1)
```

We now have accelerometer values that are read and are translated to LED colors.  A quick diversion into math and then we'll add in Bluetooth.

### A diversion: math

One thing we can use accelerometer values for is visualizing a model in space.  Typically what one does in this situation is to convert the acceleration values over to rotations.

HOWEVER.

In doing so, we actually lose a degree of freedom - we're actually going to need an *additional sensor* to calculate yaw.  So, we can only calculate roll and pitch!  This is because we're using the `x`, `y`, and `z` values to calculate roll and pitch.  If you wanted to get yaw as well you'd need a gyro sensor (not included on the Bluefruit).

If you are interested, here are a few explanations:

* [Accelerometer data: How to interpret?](https://stackoverflow.com/questions/5871429/accelerometer-data-how-to-interpret)
* [How to estimate yaw angle from tri-axis accelerometer and gyroscope](https://robotics.stackexchange.com/questions/4677/how-to-estimate-yaw-angle-from-tri-axis-accelerometer-and-gyroscope)
* [Possible to convert accelerometer x,y,z measurements into quaternion?](https://physics.stackexchange.com/questions/578359/possible-to-convert-accelerometer-x-y-z-measurements-into-quaternion)

The first link actually lets us understand why when you start rotating it fully around an axis that it slides back - the accelerometer values go back to home, meaning any rotation angle calculated will go from 0 to 180 and then back to 0 (rather than going the full 360 degrees).

<div align="center">
<img alt="X axis rotational gravity" src="https://i.stack.imgur.com/vMLJc.png" />
</div>


The next bit is interesting in terms of using those values.  To get rotational angles from accelerometer values we can transform them into quaternions (or, rotational angles that use imaginary numbers).

We would get the rotational angles (*ϕ* -> roll, *θ* -> pitch) like so (c/o the StackOverflow link above):

<div align="center">
  <img src="/gvsu-cis373/assets/images/roll-pitch-1.png" alt="roll and pitch angles" />
</div>

And then convert it to the quaternion for roll (a similar equation exists for pitch):

<div align="center">
  <img src="/gvsu-cis373/assets/images/roll-pitch-2.png" alt="roll and pitch angles 2" />
</div>

Those values would then be fed into a 3D engine (we'll use WebGL/ThreeJS later in this lab) to rotate whatever model we have loaded in.

## Second, live updates in the terminal

There are **innumberable** things you can do with all the sensors at hand.  However, without additional displays or capabilities it is difficult to communicate what is happening.

Let's go ahead and make a live terminal.  This is something that involves ASCII code trickery that enables you to use the terminal without having to print a million lines, and relies on escape codes.

Unfortunately, support for the codes varies from machine to machine and terminal to terminal, so there's a pretty good possibility that none of the color codes will work in your serial terminal (i.e., popping open Serial in Mu).  

Ok, let's extend your current code.  We want the accelerometer values to be printed to serial without scrolling off the screen.

Comment out the `print((x, y, z))` statement.

Replace it with:

```python
print(f"\33[K{x}, {y}, {z}")
print("\33[1A", end="")
```

{: .note }
In the lines above, **be careful** with auto-complete as you don't want an ending square bracket.  

So, what you should be seeing is a line being updated.  The `\33[K` erases to the end of the line, and the `\33[1A` moves the cursor up a line.  Replace the `1` with the number of lines you want it to move up (so if you wrote out 5 lines, then it'd be `5A`).  The `end=""` line suppresses newlines.

Ok, let's get you prepped to do some nicely formatted outputs.  You'll get a taste here and then you'll be extending it for the homework.

Two things we want to do are to use tabs to provide a nice output format and truncating the output so that we only show a certain amount of precision.

Update your print statement again to lop off precision:

```python
print(f"\33[K{x:.3f},\t{y:.3f},\t{z:.3f}")
```

And we can break it up a touch to make the formatting a bit nicer.

```python
print(f"\33[KAccelerometer values")
print(f"\33[KX: {x:.3f}")
print(f"\33[KY: {y:.3f}")
print(f"\33[KZ: {z:.3f}")

print("\33[4A", end="")
```

{: .note }
Note the placement of the `X:` string - looks odd but that's where you'd put a non-variable if you wanted it to start at the beginning.  Additionally, note that the last line is now `4A`...



## Third, talking to a browser

Browsers have introduced the capability to use Bluetooth connections to talk to webpages!  For reference, I'm not expecting you to manually code up a website to talk via Bluetooth though - that's outside the scope of the course.  However, I did create a page for use in another class (Computer Graphics - which does involve HTML/JavaScript) that we can use to test out our device.  It uses ThreeJS (WebGL) to render the [model of our devices](https://github.com/adafruit/Adafruit_CAD_Parts/blob/main/4333%20Circuit%20Playground%20Bluefruit/Circuit%20Playground%20Bluefruit.stl) and rotate based on accelerometer data.

(And if you're curious, it involve translating accelerometer values to quaternions).

{: .note }
Google has a pretty decent writeup on the overall tech: [Communicating with Bluetooth devices over JavaScript](https://developer.chrome.com/docs/capabilities/bluetooth).

In general, we'd be talking over GATT (Generic ATTribute Profile) - a way for Bluetooth Low Energy devices to transmit data: [GATT](https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt#services-and-characteristics).  It involves using pre-baked "templates" for transmitting known sensor data (you can always inject your own values into existing categories if you need, or write your own service).

HOWEVER, GATT is a bit of a pain with Circuit Python currently.  Fortunately for us, somebody mocked up a UART connection for JavaScript that we can use as a basis: [Web Device CLI](https://github.com/makerdiary/web-device-cli)

So what we need to do is:

1. Create the Bluetooth connection to the browser
2. Instantiate a UART connection to that Bluetooth connection
3. Package up our data and send as we did before when talking to our phones
4. While we are looping, periodically check if a connection has been dropped and re-instantiate (i.e., we clicked 'Disconnect' in the browser)

First, pop open the webpage: [https://efredericks.github.io/gvsu-cis367/demos/bluefruit-bluetooth.html](https://efredericks.github.io/gvsu-cis367/demos/bluefruit-bluetooth.html)

{: .warning }
You must do this on a device that has Bluetooth!  Lab computers will not work!  If you are using a lab computer either try your phone or wait until you're home to verify - you can at least get the code in place and functioning while you're in the lab!

{: .note }
Make sure that Bluetooth is enabled on your browser.  I see this in Firefox: `WebBluetooth API is not available.  Please make sure the Web Bluetooth flag is enabled.`  Unfortunately Firefox doesn't natively support it, so swap to a different browser like Chrome.  If it is still disabled make sure that experimental features are allowed.  See [Manjaro Forums - Can’t use Web Bluetooth in google chrome](https://forum.manjaro.org/t/cant-use-web-bluetooth-in-google-chrome/103496).

Our imports:

```
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.nordic import UARTService
```

Directly above our forever loop:

```
# Instantiate Bluetooth connection
ble = BLERadio()
ble.name = "MYLASTNAME_Bluefruit"
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("Waiting to connect...")
ble.start_advertising(advertisement)
while not ble.connected:
    pass
print("Connected")
```

Inside our forever loop (or, how to reconnect if we lost a connection):

```
# Reconnect
if not ble.connected:
    ble.start_advertising(advertisement)
    print("Reconnecting...")
    while not ble.connected:
        pass
    print("Connected")
```

The last bit then is to send off our data!  One thing you might recall is that UART seems to limit the string length (when sending data over to our phones it might split into multiple lines...).

This is a bit of an issue if we don't want to add in a ton of string parsing and/or packet management, so we'll just split up our measurements for X, Y, and Z at the cost of some extra packet sends.

{: .warning }
This probably would not be a great idea in a larger, production-ready setup!

We already have our accelerometer readings, right?  Package and send!

```
uart.write("x:{0}".format(x))
uart.write("y:{0}".format(y))
uart.write("z:{0}".format(z))
```

We are sending the `x:` portion of the string so the JavaScript application knows which axis is being sent.  Essentially, it is splitting the received string on `:` and then looking at the first value (along with some error checking).

{: .warning }
If you include spaces or otherwise deviate from the format above, the visualization **will not work**.

It should look like this after you successfully connect your device!

<div align="center">
  <img src="/gvsu-cis373/assets/images/accel_connect.jpg" alt="Accelerometer Bluetooth connection to UART" />
</div>

{: .note }
If your device seems wonky in terms of how it reacts, check the orientation of the connectors.  That will help!  Double note - recall we don't have yaw, so it isn't going to be a one-to-one representation.

## The homework

For the lab, you have read the accelerometer, mapped it to LEDs, and sent data off to a webpage via Bluetooth.

Last week, we did a bit about security (ahead of schedule, oddly enough).  Take your accelerometer values and encrypt them (print them to the terminal though)!

### Want extra credit?  Have your LEDs react to the direction you're tilting the device.

In the beginning of the lab we were setting LEDs based on a fairly naive check of our accelerometer data. One thing you could do is implement a "marble" type game where your accelerometer controls the position of the marble (pretend you have a marble on a board and tilting it changes its position).

*Note: you probably don't need all x/y/z values to make this work...*

So, what I'd expect to see here is a single LED lit up and moving about based on the orientation of the device - random movement isn't going to count!

**Tell me in your report that you did this otherwise I will not be looking for it!**

# References

* [Adafruit - Acceleration](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration)
* [Using the Accelerometer with CircuitPython: Adafruit Circuit Playground Express](https://core-electronics.com.au/guides/using-the-accelerometer-with-circuitpython-adafruit-circuit-playground-express/)
* [Bluetoooth UART](https://learn.adafruit.com/circuitpython-ble-libraries-on-any-computer/ble-uart-example)
* [Adafruit - NeoPixels](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/neopixels)
* [Communicating with Bluetooth devices over JavaScript](https://developer.chrome.com/docs/capabilities/bluetooth)
* [GATT](https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt#services-and-characteristics)