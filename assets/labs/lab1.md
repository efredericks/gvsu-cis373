---
layout: page
title: Lab 1
nav_exclude: True
description: >-
    Lab 1 page.
---

# Lab 1 - Getting Started

This lab has you getting everything ready to go to work on your Circuit Playground Bluefruit!  We are going to need to install the Mu Editor, get libraries installed, and then do some basic introductory-type things to ensure that your device is happily blinking along.

We're going to be doing a "lot" of things here, but hopefully they'll soon become second nature to you.  In theory, you should only need to install Mu once, and the libraries as-needed.  The rest you hould be able to continue using throughout the semester!

{: .new } 
> Note: this page is an excellent resource for getting you up and running if you have any issues: [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all)

## Install Mu Editor

{: .highlight}
You can use other editors, however not all of them are good/appropriate.  Mu is the suggested one out of the box and provides a lot of nice features for our specific purposes.  Check the link above for a list of recommended editors if you want to try something else!

Grab the latest installer for the Mu editor: [https://codewith.mu/](https://codewith.mu/).  If you are installing this on a lab machine you should (in theory) be able to install it to your user account.  If you are using your personal laptop install it a you normally would any other program.

(If you get stuck, here is Adafruit's Getting Started guide: [https://learn.adafruit.com/adafruit-circuit-playground-express/installing-mu-editor](https://learn.adafruit.com/adafruit-circuit-playground-express/installing-mu-editor)).

After you get it installed, we need to set it up for our device and for the Circuit Playground.

**At this point, ensure your Circuit Playground is plugged into your device with the appropriate USB connector.**

**Appropriate means it has a data line!  A normal USB charger will not work!**

## Install CircuitPython and Libraries

I don't have your kits exactly - so it may make sense to check your bootloaders are up to date and that CircuitPython is installed.

This is from the [Adafruit guide](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all#):

> To check whether you need to update the bootloader, double-click the reset button, and look in the ...BOOT drive for INFO_UF2.TXT. Inside that file, check the version number. It should be 0.6.1 or newer. 

{: .warning }
Note: I did this on my device and it temporarily shows the bootloader files.  It **should** not delete things that you may already have on there, if you've already done it.  That being said, it doesn't hurt to backup your code files if you're concerned.

When you plug in your device, you should see a `CIRCUITPY` folder popup.  If you do not, then we need to install Circuit Python.

{: .important }
> **FOLLOW THIS GUIDE TO SETUP CIRCUIT PYTHON**: 
> 
> [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython)

And then...

{: .important }
> **FOLLOW THIS GUIDE TO SETUP CIRCUIT PYTHON LIBRARIES**:
>
> [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuit-playground-bluefruit-circuitpython-libraries](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuit-playground-bluefruit-circuitpython-libraries)


## But first...

One thing to keep in mind with CircuitPython is that the file `code.py` is what runs automatically. You can have any number of files stored (within the storage limits) on your device, however only the one named `code.py` will run.

--- 

As such, we will be following a naming scheme for all of your files so that I can test them out on my device.  

Ensure that, when you submit your code to Blackboard, you name it: `code.hw[assignment-number].[your-last-name].py`

For example, if I were to submit this myself I would name it: `code.hw1.fredericks.py`.

**HOWEVER**, don't name it until you're ready to submit to Blackboard - remember it needs to be named `code.py` to make it run on your device!

--- 

Each file should also start with a header block as follows (you'll be docked points throughout the semester for missing/invalid header blocks).  If you aren't familiar, the `"""` block is a multi-line comment in Python.

```
"""
Author: <your full name>
Date: <date of submission>
Title: <title of assignment>
Description: <what this file is supposed to be doing>
"""
```

Again, for example:

```
"""
Author: Erik Fredericks
Date: 01/01/2024
Title: Homework 1
Description: This program prints timing data to the serial port, randomly blinks LEDs, and turns the LEDs on and off with button presses.
"""
```

## Get some feedback (via serial)

First and foremost, we need the ability to *trace debug* our programs, meaning that we need to be able to print out information for easy reading.  This is pretty straightforward in Mu, though we need to enable it.  Ensure your Bluefruit is plugged in and the Mu editor is running and successfully connected to your device.

Click the large `Serial` button at the top to pop open the console.  You should see a panel open at the bottom, most likely titled `CircuitPlayground REPL` (REPL -> Read-Evaluate-Print-Loop).  Every time you save, you should see some text that looks like this - meaning that your program is restarting: 

> Code stopped by auto-reload. Reloading soon.

**Note: if you're on a Mac you might need to use `Cmd` instead of `Ctrl`.**

`Ctrl+c` will cancel the running program.  You will see text like this:

> Press any key to enter the REPL. Use CTRL-D to reload.

This drops you into a Python shell and you can interact with the device as you normally would in any Python shell. As mentioned, to restart the device hit `Ctrl+d`.

Let's print some random data and create our first program!

### Our first program

Assuming you put in the appropriate header block as above (you did, right?  ಠ_ಠ), let's create a program.

First, we're going to import the `random` and `time` libraries.  These should come pre-installed with your basic CircuitPython setup, so no need to install them.

```
import random
import time

print("Hello world")
```

If you save it now, nothing will happen other than the LEDs blink and the program just ... starts and stops and prints out the requisite text - assuming you've opened the Serial panel.  Huzzah.

{: .highlight }
An aside - typically in Python you only import the aspects of the library you need.  I'm being intentionally lazy above, however by importing the **entire** `time` and `random` libraries we're taking up valuable memory space!

Let's fix that and practice proper memory usage.  Change that block to:

```
import random
from time import sleep

seconds = 0
done = False
while not done:
    print("Hello world - {0} seconds.".format(seconds))
    seconds += 1
    sleep(1)

    if seconds > 10:
        done = True
```

A couple things are happening here.  First, we are only importing the aspects of the library that we actually need (we'll update `random` later, don't worry).  For a rather smallish library like `time` this isn't necessarily crucial (if you go the extra mile and measure memory usage you're likely not able to see the difference), but if we are loading in multiple large libaries (e.g., NumPy, SciPy, etc.) then things will start to add up.

The second thing is we're changing our forever loop.  Instead of `while True` it is now `while not done`.  This enables us to control the loop via the `done` flag - this is a tactic I typically use in video game design or any time I need a forever loop.  There's nothing inherently wrong with using a `while True ... break` type of setup, however I like this approach myself.  Ergo, this is what you'll mostly be seeing (if we want the program to end, that is).

Ok, we have printed things to serial, mucked about with the REPL, now it is time to update those blinking LEDs.

## Make those LEDs blink

For reference, I want you to realize how easy life is with the Neopixel ring on your device.  You are being saved the headache of wiring, powering, and addressing them that one normally would (say, with an Arduino).  Just nod in satisfaction and move on.
 
{: .highlight }
Alternatively, look up a [Neopixel wiring guide](https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all) if you're wondering.

We need some extra libraries!  We're going to import the `board` and `neopixel` libraries.  `board` and `neopixel` are going to be used for managing those LEDs.  We'll also be using `board` later for handling button presses - essentially it is our access point into the board's connections.

First, add in the imports:

```
import board
import neopixel
```

Now, prior to our forever loop we need to initialize the Neopixel ring.  We're going to access it via a variable (`pixels`), tell its contructor how many LEDs there are (this library supports other arrangemenets as well), set its brightness, and require that we manually tell the LED array to update.  The last option allows us to speed things up by sending a single signal with a batch of changes, rather than one at a time.

```
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)

# set pixels to off initially
for i in range(10):
    pixels[i] = (0, 0, 0)

pixels.show()
```

This brings us to the concept of RGB values for color.  Essentially, 0 is black, 255 is white, and the values in between are how dark or light you want that particular value.

Our Neopixels use a tuple for RGB - `(R, G, B)`.  For instance, setting an LED to `(255, 0, 255)` will make it hot pink (or, the *magic color*).

Try setting a single pixel to a specific color.  Remember, our LEDs are indexed between 0 and 9, and each has a color specified as a 3-tuple.  Don't forget to call `pixels.show()` once you're done!

## Garbage collecting

This will be a short little bit.  Let's monitor our memory over time.  First, remove the exit condition in our `while` loop - we want this to run forever (i.e., remove the `if seconds > 10` block).

Then, at the top:

```
import gc
```

And in the body of our loop:

```
print("Hello world - {0} seconds.  We have {1} bytes available for use.".format(seconds, gc.mem_free()))
```

You may notice that ... available memory goes down over time (let it run for a while).  Our setup isn't automatically garbage collecting.

Now, at the bottom of the loop add:

```
gc.collect()
```

And if everything is working as intended, our free memory shouldn't really change all that much over time.  **You'll most likely want to garbage collect from here on out!**

{: .note }
Here is some additional information on memory management: [https://learn.adafruit.com/Memory-saving-tips-for-CircuitPython/ram-saving-tips](https://learn.adafruit.com/Memory-saving-tips-for-CircuitPython/ram-saving-tips)

## Handle button presses

We've done a lot in this introductory material, but the goal is to get you up and running as soon as possible.  The last piece for this module is to handle button presses.  The Bluefruit has two buttons built into the board - `A` and `B`.  Per usual, we need a library to handle things:

```
import digitalio
```

We're also going to define variables to initialize the buttons in-code.  This will involve adding a reference and setting if it is [pull-up or pull-down](https://www.circuitbasics.com/pull-up-and-pull-down-resistors/).  More than likely, we'll get into debouncing another time (or, how often the button "fires" while you're pressing it).

Add this above your forever loop (we only want to set it once):

```
btnA = digitalio.DigitalInOut(board.BUTTON_A)
btnA.switch_to_input(pull=digitalio.Pull.DOWN)

btnB = digitalio.DigitalInOut(board.BUTTON_B)
btnB.switch_to_input(pull=digitalio.Pull.DOWN)
```

Things to note - our variables for the buttons are `btnA` and `btnB`.  My preference is to preface variables with the hardware they represent, but this is up to you as long as it is readable (to me).

We're also setting them to be pull-down - you'll have to look this up separately as to why.

Now, let's check for button presses!  Put this in your forever loop:

```
if btnA.value:
    print("Button A pressed!")

if btnB.value:
    print("Button B pressed!")
```

You should note that, while yes it does work - there are some oddities.  However, we're handling them!  Note that there is a `value` attribute on the button element - there are others that I'll leave as an exercise to the student to research.

## Putting it together - Color Cycler

At this point let's do a little cleanup.  I'm going to give you the *general* structure of what your code should look like, but not the "full" code:

```
- comment block

- imports

- variable initializations

- LED initializations

forever loop:
  - print some information
  - delay 
  - garbage collect
```





## How do we submit the files?

You're going to need to submit your Python script to Blackboard as well as a lab manual.  I'm going to test your program by running it on my device that is identical to yours - meaning if it doesn't work on mine, then it definitely doesn't work on yours.  

If you are struggling please reach out!

## Homework

See Blackboard for the homework questions.  You have to turn your code in as well!

## Addendum

Note: I am **not** going to do this for most labs, however for the purposes of getting you up and running here is a minimum working example (if you simply copy and paste this things should work - however you aren't going to get full points for it):

```
```