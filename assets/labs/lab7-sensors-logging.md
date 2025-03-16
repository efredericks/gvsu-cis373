---
layout: page
title: Lab 7
nav_exclude: True
description: >-
    Lab 7 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 7 - Sensors (with logging!)

Last week you got your temperature and light sensors working.  Clearly, not optimal for **real** deployments, but good enough for a reasonable check (especially if you control for sensor interactions).

This week, let's do some data storage.

{: .warning }
What we're doing in this lab can **corrupt your files** if you aren't careful.  BEFORE YOU START, BACKUP EVERYTHING ON YOUR DEVICE TO YOUR PERSONAL COMPUTER.

Ok, let's get into it. 

{: .warning }
Did you back up your files yet?

<div align="center">
  <img src="https://community.atlassian.com/t5/image/serverpage/image-id/1322iB5C923CDC96E6476" alt="do it now" title="do it now" />
</div>

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Data being stored on your device

## Getting started

We're going to be working from this guide mainly, in case if you get lost or want additional details: [https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-storage](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-storage)

(Note, if you have a Bluefruit and you want to work with the Bluetooth protocol, [last year's lab](/gvsu-cis373/assets/labs/prior/lab5) dealt explicitly with this.  However, the Circuit Playground Express only has infrared and unfortunately we can't guarantee that your personal devices have an IR receiver, so I'll leave you with [this guide](https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python/overview) if you want to explore more.)

## Developing locally

For this lab, we are going to write code on your own computers and then manually copy them over to the Circuit Playground.  The reasoning for this is that (1) if your computer is playing nicely you'll have permission denied errors if you try to live-edit code and (2) if your computer allows you there is a good chance that you'll brick your device.

You can use whatever dev environment you want, including just a text editor (as long as you recall Python's spacing requirements).

So, create a folder **on your computer** and create two empty files, a `boot.py` and a `code.py` file.  

## boot.py

We're going to use the [code from Adafruit](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-storage#boot-dot-py-2985239) to setup our devices for writing.  The way it is written will allow the device to be in 'CircuitPython edit' mode (i.e., allowing local data storage through code) if the switch is to the right (near the ear icon, returning `False`) and in 'computer edit' mode (i.e., what we're used to for live-editing code) if the switch is to the left (near the music icon, returning `True`).

I updated the code slightly for our devices specifically - it is the same for the Bluefruit and Circuit Playground Express.  We don't need the commented lines for the other board types (unless, you end up getting one later on):

```python
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

# For Circuit Playground Express, Circuit Playground Bluefruit
switch = digitalio.DigitalInOut(board.D7)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=switch.value)
```

Now, let's focus on the code itself.  Still editing locally *on your computer*, pop open `code.py`.

## code.py

We're going to start with the pre-baked code from Adafruit and then you'll be modifying it for your homework.  Recall from last week that we sensed temperature **and** light - right now we're just sensing and logging temperature.  You'll be adding light later.

Here is the boilerplate code for `code.py`:

```python
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging example"""
import time
import board
import digitalio
import microcontroller

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.switch_to_output()

try:
    with open("/temperature.txt", "a") as fp:
        while True:
            temp = microcontroller.cpu.temperature
            # do the C-to-F conversion here if you would like
            fp.write('{0:f}\n'.format(temp))
            fp.flush()
            led.value = not led.value
            time.sleep(1)
except OSError as e:  # Typically when the filesystem isn't writeable...
    delay = 0.5  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.25  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)
```

So, some things are different than what we're used to.  First, we're using the on-board LED (not your Neopixels) to indicate something is happening.  A lot less *in your face* this way.  You are welcome to use your LED code from before, naturally.

Also, we're using a different temperature sensor.  Hmm...

<div align="center">
  <img src="/gvsu-cis373/assets/images/spinning-hmm.gif" title="spinning hmm gif" alt="spinning hmm gif" />
</div>

## Copying over and checking output

At this point, you should have a `boot.py` and `code.py` file setup locally <strong><font color="red">and your prior code backed up somewhere safe</font></strong>.

Now, here's how this will work.  Recall the logic for the switch.  We only want CircuitPython to be able to write to the device, so flip your switch over towards the ear icon, plug it in, and copy over the `boot.py` and `code.py` files you created.

{: .important }
`boot.py` only runs **once** on startup - if you want it to run again you need to eject the Circuit Playground from your computer and disconnect it!

You should see the little red light blinking after a few moments - if you don't try hitting the `reset` button.  If that still doesn't work make sure the switch is in the right place, unplug/replug the device, and try again.

You should also see a `temperature.txt` file popup on your `CIRCUITPY` drive.

{: .note }
Open the file - depending on your operating system this *might* be different, but notice that the file isn't updating.  Why do you think this might be?

So now, if you want to get the file, eject/unplug your device again, switch the switch over to the other side (so that we don't keep updating the file), and copy it over to your computer.  You should see a *lot* of data!  Just think of the graphs you could make, trends you could analyze, etc.

## Your homework!

Change the output to include both CPU temperature and the sensor-based temperature and light sensors we used in the last lab.
The format of your output data should look like this (including line headers), and the name of the file should be `yourlastname-sensor-log.txt` (obviously replacing `yourlastname` with your actual last name).  The ellipses indicate additional lines of data.  The temperature should be in Celsius (i.e., you do not need to convert to Fahrenheit).

Truncate each sensor reading to 2 decimal points.  The print statement you need for that is (there are multiple ways to do this, choose one you're happy with):

For example, the easiest (to me) would be to update the variable (or create a temporary variable) with the rounded value:

`temp = round(temp, 2)`

Additionally, include the current timestamp (so we know when the readings happened).  You can use this call to get the current time from the start of the program:

`time.monotonic()`

{: .note }
For simplicity's sake we're just going to use an arbitrary time from the start of the program.  However, if you wanted to 'do better' you could include the datetime library from Adafruit: [https://docs.circuitpython.org/projects/datetime/en/stable/api.html](https://docs.circuitpython.org/projects/datetime/en/stable/api.html)

Your output should resemble this:

```
Time,CPU Temperature,Sensor Temperature,Light
1.33,23.0,25.92,752
2.5,23.0,25.89,480
...
```

## Extra credit opportunity!

Incorporate last week's code into this lab.  While your device is logging data above, have it also perform the light-reactive requirements from last week's lab (i.e., selecting light vs. temperature and visualizing via the LEDs). 

## Double Extra credit opportunity!

Graph your output in some fashion (using Excel, Python's `matplotlib` or `seaborn` libraries, etc.).  See if there are any trends in your data!  Include your plots and your plot-generating code/files in your homework submission.  The amount of effort will dictate how much extra credit I assign (just plots will be less than plots with a discussion or critical thinking, for example).

## If you are struggling with the file writing:

* Make sure you're **safely-ejecting** your USB device!  Yanking out the USB cord might result in filesystem issues.
* If your data file is invalid, make sure that `fp.flush()` is being appropriately called!
* If your data seems invalid, insert some `print` statements with your intended data to make sure it is working as you think it is.
