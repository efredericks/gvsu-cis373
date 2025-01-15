---
layout: page
title: Lab 1
nav_exclude: True
description: >-
    Lab 1 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 1 - Getting Started

Given that our Bluefruits are *unavailable* at the moment, we're going to run through the simulator and get up and running with the general concepts of Lab 1.  This can all be accessed via a browser.

This is the link to the simulator: [https://maker.makecode.com/](https://maker.makecode.com/)

## Lab Signoff

{: .warning } 
For each lab, I will have some minimal things you need to do before you leave for the day.  This will be part of your **participation grade**, so don't forget to do it!

Before you leave for the day, (minimally) show me:

1. The MakeCode simulator running the printing/LED example (the first one)
2. LEDs blinking in a separate project (the second one).

## Reference Guide

If you find yourself looking for a command or clarification on syntax, here is the [reference guide](https://makecode.microbit.org/reference/).

## Saving and Loading

Saving and loading projects is handled via images.  You click 'Save' on the bottom, it downloads an image, and that is your save file.  You can load projects by ... uploading the image (you have to go back to the projects list).

Note that the editor will save them to your local storage, however that won't persist across devices (unless if you setup Git repositories...).

## Install CircuitPython and Libraries

Well, this simulator actually uses block-based programming (or JavaScript, or Python) to handle things, and no installation is necessary.  Unfortunately with the quick turnaround needed to do this lab I am not as familiar with how Adafruit set up their JavaScript framework, the Python implementation is not a one-to-one comparison, so we're going to go block-based for now.  

If you ever have used Scratch you'll feel right at home.  If not, no worries. 

## Hello World

The `on start` block is the equivalent of a `setup` function in Arduino and the `forever` block is the equivalent of the `loop` function.  This doesn't really exist in CircuitPython, but think of it this way:

* `on start` / `setup` only runs once, at the start of a program (typically to initialize things)
* `forever` / `loop` runs for ever, and is the equivalent of putting a `while True` loop in your code.

Let's do some basic things.  Create a new project, call it `YourLastName-CIS373-Lab1`.  We'll be modifying it throughout this lab.

Next, pick the Bluefruit as the board.  The simulator can simulate nearly all Adafruit boards, which is nice.  Let's use the one we **should** be using in class.

You should see this:

<img alt="CircuitPlayground Bluefruit simulator" src="/gvsu-cis373/assets/images/lab1-makecode.png" />

{: .highlight }
It seems that we don't get a serial console via the simulator, so if we want to print debugging messages we'll have to use the console.  You also need to get into debug mode to see them (and exit debug mode if you want to modify the program).  

So, print `hello world`.  Drag a `console log` block into the `on start` block and add some text.  Something fun like `Hello world` or cheeky like `I wish that we all had hardware we could use this on.`

{: .highlight }
Doubly interesting - you can write programs in the simulator, download the `UF2` file, and drag it onto your eventual Circuit Playground devices (essentially, flashing it like you would have done with the CircuitPython file).

### Our first program

In the real lab, we'd be importing libraries, getting time and memory usage going, etc.  Since a lot of that will be obfuscated, let's just follow the basics.  In Python we'd be printing out something every second, then ending at 10 seconds.  We can recreate that in Makecode

This is the original:

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

Now, let's do that in the simulator.  We'll add in a notification as well - we can have the lights turn green when done.

First, create a variable in `on start` - `timer = 0`.  It should look like this.

{: .important }
I had to search for 'true' to find the Boolean variable to move into the variable assignment.  

<img alt="CircuitPlayground Bluefruit simulator setup" src="/gvsu-cis373/assets/images/lab1-setup.png" />

You might be wondering about that `done` variable.  Since we have the `forever` block we don't need to create our own.  We'll just bail out of the loop once we're ready.

Now, let's increment our variable and delay the program so it doesn't run too fast.  If you've programmed before this might be slightly confusing, but we are essentially going to be doing a `timer = timer + 1` type of call.

We also want to have our program sleep slightly so that we aren't overwhelming the device.  Confusingly, the delay is named `pause` (there is a `wait` block as well - but that is waiting for an event, not pausing the program).

It should look like this at this point:

<img alt="CircuitPlayground Bluefruit simulator printing" src="/gvsu-cis373/assets/images/lab1-printing.png" />

If you pop open the debugger you should see data being printed.

Now, if you want to have 'better' output you might want to do string concatenation.  It is a bit of a reach since you have to be *very* verbose, but it should look like this:

<img alt="CircuitPlayground Bluefruit simulator pretty printing" src="/gvsu-cis373/assets/images/lab1-printing-pretty.png" />

Last step, let's update the forever loop so that the program has an end point.  

{: .highlight }
Note: I can't find a way to fully break out of the forever loop, so we will just allow it to go forever but will make sure it doesn't "do anything" when it shouldn't.

Let's add a conditional - first we'll check if the `timer` variable is greater than 10, and if so, we'll turn the lights green.  Otherwise, we'll do our usual printing.

Add an `if` statement to make it look like this:

<img alt="CircuitPlayground Bluefruit simulator if" src="/gvsu-cis373/assets/images/lab1-if1.png" />

Should work fine, however it still prints forever.  Move the printing statements into an `else` block (you'll need to grab the `if-else` block):

<img alt="CircuitPlayground Bluefruit simulator if-else" src="/gvsu-cis373/assets/images/lab1-if2.png" />

Not bad, we now have the concepts of logic, variable setting and printing, and setting LEDs. 

{: .important }
Take a screenshot of your working simulation, including the console output and the LEDs on and save it for your lab report.

## Make those LEDs blink (with randomness)

Now, let's make them blink.  **Create a new project as we'll be starting fresh.**

Skipping the Neopixel (the LEDs) instrumentation for now, this brings us to the concept of RGB values for color.  Essentially, 0 is black, 255 is white, and the values in between are how dark or light you want that particular value.

Our Neopixels use a tuple for RGB - `(R, G, B)`.  For instance, setting an LED to `(255, 0, 255)` will make it hot pink (or, the *magic color*).

Try setting a single pixel to a specific color.  Remember, our LEDs are indexed between 0 and 9, and each has a color specified as a 3-tuple. The block-based language allows you to directly pick a color or to manually set it:

<img alt="CircuitPlayground Bluefruit simulator LED" src="/gvsu-cis373/assets/images/lab1-led.png" />

Now, let's have a randomly-selected LED blink a random color every second, ensure we clear out the prior colors.

Try to do the following steps - I'll give the final reference but try on your own:

1. Create an additional variable `led_index` to hold our randomly-selected index (keep the `led` variable as we'll use that too).  

2. Add a random number block that is `pick random 0 to 9` and copy and paste it into the `led_index` variable.

3. Add a random number block that is a `pick random 0 to 255`, copy and paste it into each of the RGB fields in `led`, and drag the initialization into the top of the forever loop.  This will give a new value each iteration rather than only one.

What you should see is a randomly-selected LED show a randomly selected color, where the colors are cleared out each loop to "refresh" the LED ring.

{: .note }
The random number block is inclusive, so doing random between 0 and 9 will yield a value on [0, 9].

Here is the [hint](/gvsu-cis373/assets/images/lab1-led-colors.png).

{: .important }
Take a screenshot of your working simulation, including the console output and the LEDs on and save it for your lab report.

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

# flags/timeres
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

    # Set our LED colors and display them, if enabled
    for i in range(NUM_LEDS):
        pass # Should handle LED display here - i.e., setting pixels array
    pixels.show()

    sleep(.01)
    gc.collect()

print("Program done - exiting.")
```