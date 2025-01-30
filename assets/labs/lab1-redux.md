---
layout: page
title: Lab 1 Redux
nav_exclude: True
description: >-
    Lab 1 Redux page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 1 - Getting Started (Again)

Supply chain resolved! We're going to go back to Lab 1 and actually do it in real hardware.

**Note: this is not identical to lab 1!  It is similar but there are some minor differences.  If you are one of the few that jumped ahead make sure you hit all the requirements.**

This lab has you getting everything ready to go to work on your Circuit Playground Bluefruit or Express!  We are going to need to install the Mu Editor, get libraries installed, and then do some basic introductory-type things to ensure that your device is happily blinking along.

We're going to be doing a "lot" of things here, but hopefully they'll soon become second nature to you.  In theory, you should only need to install Mu once, and the libraries as-needed.  The rest you hould be able to continue using throughout the semester!

{: .new } 
> Note: this page is an excellent resource for getting you up and running if you have any issues: [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit?view=all)
> Double note: if you have an Express, this is your link: [https://learn.adafruit.com/adafruit-circuit-playground-express?view=all](https://learn.adafruit.com/adafruit-circuit-playground-express?view=all)

## Lab Signoff

{: .warning } 
For each lab, I will have some minimal things you need to do before you leave for the day.  This will be part of your **participation grade**, so don't forget to do it!

Before you leave for the day, (minimally) show me:

1. The Mu editor installed and running your code.
2. LEDs active on your device.

## Install Mu Editor

{: .highlight}
You can use other editors, however not all of them are good/appropriate.  Mu is the suggested one out of the box and provides a lot of nice features for our specific purposes.  Check the link above for a list of recommended editors if you want to try something else!

{: .highlight}
In theory, it should already be installed on the lab PCs - if you are using those then you just need to make sure it works with your device!

Grab the latest installer for the Mu editor: [https://codewith.mu/](https://codewith.mu/).  If you are installing this on a lab machine you should (in theory) be able to install it to your user account.  If you are using your personal laptop install it a you normally would any other program.

(If you get stuck, here is Adafruit's Getting Started guide: [https://learn.adafruit.com/adafruit-circuit-playground-express/installing-mu-editor](https://learn.adafruit.com/adafruit-circuit-playground-express/installing-mu-editor)).

After you get it installed, we need to set it up for our device and for the Circuit Playground.

**At this point, ensure your Circuit Playground is plugged into your device with the appropriate USB connector.**

**Appropriate means it has a data line!  A normal USB charger will not work!**

{: .highlight}
At least this semester I'll be skipping Mu personally as I decided to go with Linux-only computers.  Mu is intended to be a "simple" interface for both a code editor and access to the serial console.  Mu doesn't work very nicely with Linux at present, so I will be using VSCode along with a program to monitor the serial connection (most likely `minicom`).  Don't worry about directly replicating my setup (unless if you use Linux as well!).

## Install CircuitPython and Libraries

When you plug in your device for the first time you'll most likely see a `CPLAYBOOT` or `CPLAYBTBOOT` directory pop up - this means you're in bootloader mode.  If you see `CIRCUITPY` you're most likely fine (meaning, your device is running CircuitPython).

{: .important }
We want to be running the latest version of CircuitPython - 9.x.  

If you have installed CircuitPython already and you're in bootloader mode, you should be able to hit the reset button to switch (you might need to double tap it).

{: .important }
If you PREVIOUSLY installed CircuitPython 7.x then you'll need to update the bootloader to get the latest version running - see me and I can help.  Alternatively, you can download the Arduino IDE and try to go that route if you prefer.  See [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/update-bootloader](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/update-bootloader) if you want to try.

If you have tried and you cannot install the latest version of CircuitPython, come see me and I can help you update your bootloader. 	

You will need to download an appropriate version of CircuitPython for your device.  Go here, select your device (Bluefruit or Express) and download the UF2 file of the latest CircuitPython: [CircuitPython Downloads](https://circuitpython.org/downloads)

Try to drag and drop the `uf2` file onto the `CPLAYBTBOOT` directory (double-click the `reset` button to access the drive): 

{: .important }
> **FOLLOW THIS GUIDE TO SETUP CIRCUIT PYTHON**: 
> 
> [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython)

And then...

{: .important }
> **FOLLOW THIS GUIDE TO SETUP CIRCUIT PYTHON LIBRARIES**:
>
> [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuit-playground-bluefruit-circuitpython-libraries](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuit-playground-bluefruit-circuitpython-libraries)
 
{: .note }
You want the libraries that work with CircuitPython 9.x!  The earlier libraries will not work!  Additionally, the page might be specific to the Bluefruit however the libraries should work fine regardless, as they are targeted at CircuitPython and not the device itself.

You're going to need the `neopixel.mpy` library from the above library download.  Open up the ZIP file, go into the `lib` directory, and copy `neopixel.mpy` into the `lib` directory on your device.

{: .important }
Make sure you keep that archive of libraries handy!  You'll be needing it for nearly every lab!  (Sometimes the download takes a *while*).


## But first...

One thing to keep in mind with CircuitPython is that the file `code.py` is what runs automatically. You can have any number of files stored (within the storage limits) on your device, however only the one named `code.py` will run.

--- 

As such, we will be following a naming scheme for all of your files so that I can test them out on my device.  

Ensure that, when you submit your code to Blackboard, you name it: `code.hw[assignment-number].[your-last-name].py`

For example, if I were to submit this myself I would name it: `code.hw3.fredericks.py`.

**HOWEVER**, don't name it until you're ready to submit to Blackboard - remember it needs to be named `code.py` to make it run on your device!

--- 

{: warning}
Note: sometimes copy/pasting code directly messes with alignment - double check that what you pasted follows Python alignment rules!


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
Title: Homework 3
Description: This program prints timing data to the serial port, cycles colors, and turns the LEDs on and off with button presses.
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

Let's print some data and create our first program!

### Our first program

Assuming you put in the appropriate header block as above (you did, right?  ಠ_ಠ), let's create a program.

First, we're going to import `time` library.  It should come pre-installed with your basic CircuitPython setup, so no need to install it.

```
import time

print("Hello world")
```

If you save it now, nothing will happen other than the LEDs blink and the program just ... starts and stops and prints out the requisite text - assuming you've opened the Serial panel.  Huzzah.

{: .highlight }
An aside - typically in Python you only import the aspects of the library you need.  I'm being intentionally lazy above, however by importing the **entire** `time` library we're taking up valuable memory space!

Let's fix that and practice proper memory usage.  Change that block to:

```
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

A couple things are happening here.  First, we are only importing the aspects of the library that we actually need.  For a rather smallish library like `time` this isn't necessarily crucial (if you go the extra mile and measure memory usage you're likely not able to see the difference), but if we are loading in multiple large libaries (e.g., NumPy, SciPy, etc.) then things will start to add up.

The second thing is we're changing our forever loop.  Instead of `while True` it is now `while not done`.  This enables us to control the loop via the `done` flag - this is a tactic I typically use in video game design or any time I need a forever loop.  There's nothing inherently wrong with using a `while True ... break` type of setup, however I like this approach myself.  Ergo, this is what you'll mostly be seeing (if we want the program to end, that is).

Ok, we have printed things to serial, mucked about with the REPL, now it is time to update those blinking LEDs.

## Make those LEDs blink

For reference, I want you to realize how easy life is with the Neopixel ring on your device.  You are being saved the headache of wiring, powering, and addressing them that one normally would (say, with a *standard* Arduino).  Just nod in satisfaction and move on.
 
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
NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, auto_write=False)

# set pixels to off initially
for i in range(NUM_LEDS):
    pixels[i] = (0, 0, 0)

pixels.show()
```

This brings us to the concept of RGB values for color.  Essentially, 0 is black, 255 is white, and the values in between are how dark or light you want that particular value.

Our Neopixels use a tuple for RGB - `(R, G, B)`.  For instance, setting an LED to `(255, 0, 255)` will make it hot pink (or, the *magic color*).

Try setting a single pixel to a specific color.  Remember, our LEDs are indexed between 0 and 9, and each has a color specified as a 3-tuple.  Don't forget to call `pixels.show()` once you're done!

## Oh so bright!

To avoid burning your eyes out, you can change the brightness.  When you initialize the NeoPixel ring you can set it on a scale between 0.0 and 1.0:

```
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, auto_write=False, brightness=0.2)
```

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

{: .note }
We're using the built-in buttons here.  You can wire/clip a button to any of the open ports you see ringing your device for additional inputs!  In a future lab we may even use some *non-traditional* methods of input.

Now, let's check for button presses!  Put this in your forever loop:

```
if btnA.value:
    print("Button A pressed!")

if btnB.value:
    print("Button B pressed!")
```

You should note that, while yes it does work - there are some oddities.  However, we're handling the buttons!  Note that there is a `value` attribute on the button element - there are others that I'll leave as an exercise to the student to research.

The one second delay at the end of the loop must be dreadfully annoying though.  Change the delay at the end of the loop to:

```
sleep(0.01)
```

You can also comment out the `print` statement as well since we don't need it anymore.

Now your button presses should be a bit nicer.  If you want to understand what I mean by *nicer* try the next section with the delay of one second.  

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

### What our goals are:

Let's plan this out a bit - we want to (1) define an array of colors, (2) set one of our buttons to cycle through the colors, (3) set the other button to turn the lights on and off, and (4) set *both* buttons to end the program.

### (1) Define an array of colors

There most likely is a CircuitPython library that I'm not aware of (please feel free to let me know if you find one) that defines colors, so we're going to manually define a set of colors as well as our colors array.  We also need a "current index" to track which color to show.

First up, define the available colors - remember we have the range of [0, 255] for each color component.  Feel free to add additional colors as well.

```
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)
```

{: .note }
An RGB color code chart is quite helpful if you want to figure out what colors to use!  [https://www.rapidtables.com/web/color/RGB_Color.html](https://www.rapidtables.com/web/color/RGB_Color.html)

We'll also need our index value:

```
color_index = 0
```

And our array (note we're leaving off `BLACK` as we'll use that as our clear color):

```
colors = [RED, GREEN, BLUE, WHITE, PINK]
```

Now, any time you want to set your colors you can use human-readable values.  For example, LED0 can be set to hot pink by writing `pixels[0] = PINK` or `pixels[0] = colors[4]`

### (2) Set one button (`button A`) to cycle through colors

Now, let's go ahead and use `button A` to cycle through our colors array! What we're going to do is update our new color index variable each time that button is pressed, and ensure we check if it goes out of range (you wouldn't want to access an array element that doesn't exist, would you? ಠ_ಠ).

Inside your `if btnA.value` conditional:

```
# Cycle through colors
if btnA.value:
    color_index += 1
    if color_index > len(colors)-1: 
        color_index = 0
```

By defining our check in this fashion, we could make our `colors` array as large as possible without needing to rewrite this code.  So now, we naturally need to do *something* with `color_index`, right?

---

For ease of use, we're going to set the LED colors every loop cycle.  A better way would be to turn this into a function and only set them when we do some event, but we'll save that for a future assignment.

For now, in the main body of the loop (right above the call to `sleep(0.01)`):

```
# Set our LED colors and display them
for i in range(NUM_LEDS):
    pixels[i] = colors[color_index]
pixels.show()
```

You should see your LED ring start out as RED and cycle through each color every time you press `button A`.

HOWEVER, it is probably going *ridiculously* fast.  Let's add a *short* delay to our button presses (i.e., a naive debouncing).

#### ADDING A DELAY

This is an interesting conundrum.  We have our `sleep(0.01)` call at the bottom of our loop to slow things down.  However it is still too fast for our buttons.  One thing we can do is to add a short delay on our button presses (something you might see often in, say, video games, to reduce the amount of times something happens when pressing a button).

First of all, define a variable at the top to handle our delay:

```
btn_timer = 0  # press rate
```

And then, update your conditional:

```
# Cycle through colors
if btnA.value and btn_timer == 0:
    btn_timer = 15  # cooldown rate

    color_index += 1
    if color_index > len(colors)-1: 
        color_index = 0

# Handle button cooldown 
if btn_timer > 0:
    btn_timer -= 1
```

{: .note }
It would be smarter to define `15` as a global variable since we'll be using it in multiple places - this avoids the possibility of mistakes with timers.

Ok, now we have a short timer that basically "locks" the button until we want it to fire again.  This is a "feel" thing - if it is too fast make that value larger - if too slow make it smaller!  We'll do the same for `button B` as well in the next section.

### (3) Set one button (button B) to turn lights on and off

This one is pretty straightforward.  We're going to define a *flag*, or a variable that is boolean in nature, to define our light state.

In your variable initialization area, add the following:

```
lights_on = True  # flag to enable/disable lights
```

And modify the button B press code:

```
# Toggle light state
if btnB.value and btn_timer == 0:
    lights_on = not lights_on
    btn_timer = 15
```

And then modify the light showing code:

```
# Set our LED colors and display them, if enabled
for i in range(NUM_LEDS):
    if lights_on:
        pixels[i] = colors[color_index]
    else:
        pixels[i] = BLACK
pixels.show()
```

What is happening here is that we're setting our values, and if the B button has been pressed we're setting the color to `BLACK` (or (0, 0, 0)), which is off for LEDs.

### (4) Set both buttons (buttons A and B) to end the program

Oddly enough, this is the easiest bit of code.  However, we need to put it in a special place, otherwise we'll see odd behavior.

Right before you check the button values, add the following conditionals and move your pre-existing button presses into the `else` block:

```
if btnA.value and btnB.value: # Both buttons pressed - exit
    done = True
else: # Handle button presses as normal
    if btnA.value and btn_timer == 0:  #...
```

Now **why** did we have to do the exit check first?  We don't want the pre-existing code for `btnA` and `btnB` to run as well as our exit code.  

### (5) Set the switch (D7) to toggle the brightness

For handling the switch (input D7) we need to initialize it and set its direction/pull status.  Add this after your button definitions:

```
switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
```

And you can simply check its state by looking at `switch.value` - it will be Boolean.  If it is `True` set the brightness high, else set it low.  Recall that you can set brightness directly by setting `pixels.brightness`, and it will be on a range of `[0.0, 1.0]`.


## How do we submit the files?

You're going to need to submit your Python script to Blackboard as well as a lab manual.  I'm going to test your program by running it on my device that is identical to yours - meaning if it doesn't work on mine, then it definitely doesn't work on yours.  

If you are struggling please reach out!

## Homework

See Blackboard for the homework questions.  You have to turn your code in as well!


## Addendum

Note: I am **not** going to do this for most labs, however for the purposes of getting you up and running here is a minimum working example (if you simply copy and paste this things should work - however you aren't going to get full points for it):

```
"""
Author: Erik Fredericks
Date: 01/01/2024
Title: Homework 1
Description: This program prints timing data to the serial port, randomly blinks LEDs, and turns the LEDs on and off with button presses.
"""

from time import sleep
import board
import neopixel
import gc
import digitalio

### board initialization

# initialize neopixels
NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, auto_write=False)

# available colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)

color_index = 0
colors = [RED, GREEN, BLUE, WHITE, PINK]

# flags/timers
lights_on = True    # flag to enable/disable lights
btn_timer = 0       # press rate


# set pixels to off initially
for i in range(NUM_LEDS):
    pixels[i] = BLACK
pixels.show()

# setup buttons
btnA = digitalio.DigitalInOut(board.BUTTON_A)
btnA.switch_to_input(pull=digitalio.Pull.DOWN)

btnB = digitalio.DigitalInOut(board.BUTTON_B)
btnB.switch_to_input(pull=digitalio.Pull.DOWN)

switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

### forever loop
done = False
while not done:
    if btnA.value and btnB.value: # Both buttons pressed - exit
        print("Should handle exit condition here")
    else:
        # Cycle through colors
        if btnA.value and btn_timer == 0:
            print("Should handle button A press here")
            btn_timer = 15

        # Toggle light state
        if btnB.value and btn_timer == 0:
            print("Should handle button B press here")
            btn_timer = 15

    # Handle button cooldown
    if btn_timer > 0: btn_timer -= 1

    # Handle brightness with a toggle
    if switch.value:
        pass # set pixel brightness high
    else:
        pass # set pixel brightness low

    # Set our LED colors and display them, if enabled
    for i in range(NUM_LEDS):
        pass # Should handle LED display here - i.e., setting pixels array
    pixels.show()

    sleep(.01)
    gc.collect()

print("Program done - exiting.")
```
