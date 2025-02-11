---
layout: page
title: Lab 3
nav_exclude: True
description: >-
    Lab 3 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 3 - Synthesizers with friends!

This week we're going to be making beats and mixing it up with friends in Interactive Media.  They'll be bringing extra things to connect, samples to play, and a fresh perspective on devices in our lives - you'll be programming the synthesizer.

(If you're wondering where this fits into a pervasive computing course, think embedded devices, human interaction, and localized sensing).

## Lab Signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

1. Your beats (your progression of button presses, written down), light show included, and demo what you've done for the day!

2. An idea (napkin-style, written down, and discussed with me) for how to use embedded devices in a *meaningful* project. **You need to submit two for your writeup by tomorrow night!**

## A Brief Word

This lab session is intended to take up the entire course period and you are welcome to work through it at your own pace.  At each step explore what is possible - change values, try things out.  Your goal today is to really make this board work for you.

Note - if you are feeling particularly explorative there are other things on the board you could look into ... a slider, accelerometer, temperature sensor, etc.  (Sensors we'll do next week).

## Setup

**As usual, make a backup of your code from last week (if you haven't already)**.

We're going to start off with using your touch pads and buttons on your device.  

Here is some boilerplate code (that you've already written before).  It comprises the imports we'll need and your forever loop, along with handling buttons and touch.

```
from time import sleep
import board
import neopixel
import gc
import digitalio
import touchio

# initialize neopixels
NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, brightness=0.05,auto_write=False)

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
    sleep(.01)
    gc.collect()

print("Program done - exiting.")
```

{: .highlight }
Walk your new partners through your device, its capabilities, what we're doing here in this section, etc.  

### Audio Imports

Let's get setup for audio now.  Add the following imports:

{: .note }
These are intended to be board-independent, hence the "fallback" imports!

```
try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

# Setup audio variables and enable speaker 
bpm = 120 
audio = AudioOut(board.SPEAKER)
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True


# Helper function to play a specified audio file
def play_file(filename):
    print("Playing file: " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)
    sleep(bpm / 960)  # Sixteenth note delay
```

These are going to give us access to (1) loading in WAV files (i.e., sound sample), (2) the audio port on our device (either the onboard speaker or that lovely `AUDIO` pad that we will be using later), and (3) the ability to construct raw tones.  Let's start with the latter.

We also now have our first function!  `play_file` will be called whenever we press one of our touch inputs.

{: .warning }
If you look around the internet for guides you'll probably see references to the `adafruit_circuitplayground` library.  It will most likely conflict with the way we're handling the speaker as it likes to self-initialize everything.

{: .highlight }
Make sure you aren't seeing any errors in the Serial console here! 

### Tone Generator

{: .note }
This link describes the tone generator concepts pretty well - we'll be using a `sine` wave to create them:  [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-audio-out](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-audio-out)

First up, let's make some manual tones.  We'll use the buttons for these, since we'll be using the touch arrays for other things.

From the [circuitplayground community bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20240123/adafruit-circuitpython-bundle-8.x-mpy-20240123.zip), copy over the `adafruit_waveform` folder into your `lib` directory on your device.

Then, let's make tones.  In the imports:

`from adafruit_waveform import sine`

And in the loop:

```
if btnA.value and btn_timer == 0:
    btn_timer = BTN_TIMER_DELAY

    sine_sample = RawSample(sine.sine_wave(220, 80))
    audio.play(sine_sample, loop=True)
    sleep(.5)
    audio.stop()
 
if btnB.value and btn_timer == 0:
    btn_timer = BTN_TIMER_DELAY

    sine_sample = RawSample(sine.sine_wave(440, 40))
    audio.play(sine_sample, loop=True)
    sleep(.5)
    audio.stop()
```

{: .note }
The `sine_wave` function expects (frequency, pitch) as inputs - try changing their values to see what happens!  Additionally, however long you `sleep` is however long that tone will play, since `loop` is set to `True`.

{: .highlight }
This is all we're doing with tones - however you're more than welcome to incorporate them into your final samples!  Use the buttons to start/stop playing the tone!  Use the touch pads to increase/decrease pitch and frequency!  Heck, create your own theramin!

### Playing Samples

Samples are small little bits of audio that will play when you activate some input.  

First, you'll need to copy the files to the device.  On your `CIRCUITPY` drive make a folder called `audio`.  Assuming your partner brought in sounds, copy those files over to the new `audio` directory.

{: .note }
If you don't have any available sounds you can grab some from Adafruit (this is on the drum machine guide): [https://learn.adafruit.com/elements/2915137/download?type=zip](https://learn.adafruit.com/elements/2915137/download?type=zip)

We need to now load them in - this is where your setup will differ from mine.

If you were using the project bundle above, we have seven files to load in.  You can load in as many as your device can handle, but remember you only have seven touch inputs (and two additional buttons...).

In our initialization area:

```
audiofiles = ["./audio/bd_tek.wav",
              "./audio/elec_hi_snare.wav", 
              "./audio/elec_cymbal.wav",
              "./audio/elec_blip2.wav", 
              "./audio/bd_zome.wav", 
              "./audio/bass_hit_c.wav",
              "./audio/drum_cowbell.wav"]
```

This makes a list of files - so if you wanted a cowbell you'd play the file stored in `audiofiles[6]`.  Remember to use the correct file names!  

{: .note }
If you're not familiar with Linux pathing, the `./audio` part means to look in the current directory (`./`) and then in the `audio` folder.  The program is looking relative to where it exists on the `CIRCUITPY` folder.

We now our files in an array to be selected upon touch.   

{: .warning }
If you are getting errors with your wav files then check with me - it is possible your file is not in the correct format - there is a guide at the bottom for ensuring you have the correct format!

Let's set it up!  You can comment out all your tone generator code - later you may wish to repurpose it for your "final" demo here.

We can be a little cheeky here - let's setup an array for our touch pins to play the associated touch file (meaning that the first touch pad will play the first audio file, and so on).

Just below the audio file load in:

```
touchPad = [touch_A1, touch_A2, touch_A3, touch_A4, touch_A5, touch_A6, touch_TX]
```

Then, our forever loop:

```
while not done:
    for i in range(len(touchPad)):
        if touchPad[i].value:
            play_file(audiofiles[i])
```

So, here we loop through all of our touch pads and play the sound file at the corresponding index.  We *could* have made this a bunch of if statements, but this is significantly shorter.  Though, a bit less flexible.

{: .note }
The eagle-eyed programmer might notice we're not checking if the files actually exist or were loaded in at all - it just kind of happens when you try to use it.  If you have a naming error, or a file error, then you won't notice it until you activate that particular file.  Not the best programming practices really!

Try out your beats!  You should hear a distinct sound for each touch pad you hit.  If you only have a few samples either download the pack from above or simply duplicate the touch pad hits.

{: .highlight }
Explore different samples and combinations.  Feel free to come up front and connect to the speakers to try things out.  Mess around with delay timing to get a better "feel" when you play a beat.

---

For starters, just try using the touch pads to make them work.  You should be hearing your tinny little beats coming out of the device (later you'll hook them up to some speakers).

This is where you can have some fun.  

{: .warning }
Remember - turn off the power before wiring things up!  You do not want to accidentally make a connection that shouldn't happen and release the device's magic smoke.

Connect up your alligator clips to all the touch pads.  You now have a bit more freedom in touching them.

Here's the diagram for what is touchable if you don't recall:

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/054/810/large1024/circuitpython_cpx_capacitive_touch_pads.jpg" alt="Touch pads">
</div>

Then, try connecting some of the random things you've brought!  Connect some pennies, hook the alligator clamps into fruit, touch it to the chair if it has metal legs.

If you have things that require piercing (like an orange) then I should have some male-male jumper wires that you can use to pierce the fruit.  

{: .note }
If you are using things that are a bit goopy then make sure you clean off the contacts before touching other things!

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/047/303/large1024/circuit_playground_play808.png?1507940432" alt="circuit playground drum machine with pennies" >
</div>

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/037/285/large1024/circuit_playground_fruit_banner.jpg?1479071905" alt="circuit playground drum machine with fruit" >
</div>

## And a Light Show

Last week we programmed our LEDs.  We haven't really done anything with them this week so far and that is just a shame.  

With your partners, come up with a lightshow to accompany your synth demo.  It can be continuously playing, reactive to your touch, whatever you'd like!  There's no "formal" requirement here other than your lights are doing *something*.

If you recall, we can set all of our lights to green via:

```
for i in range(NUM_LEDS):
    pixels[i] = GREEN
```

Remember, you can set them individually, set brightness, etc.  Just remember to call `pixels.update()` when you're ready for them to turn on each cycle!

## Demo Time!

Come up with a beat.  Write down your notes (i.e., the things you're touching).  Add a lightshow.  Come up front with your partner and demo it!

Note - the following image is for a CircuitPlayground Express.  The Bluefruit has an `AUDIO` port - use that instead of A0.
<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/047/228/large1024/circuit_playground_hp.png?1507854669" alt="wiring" />
</div>

Connect as shown - typically a black wire is used for ground and you can use any other color for the audio connection.  

{: .warning }
Make sure your device is powered off AND the volume on the speakers are turned down when making the connections!

If you have done everything correctly (i.e., your internal speaker was working earlier) you shouldn't have to change anything to get it to work on the "big" speaker.

## Napkin Ideas

Some of the best ideas are jotted down "on a napkin" when discussing with friends, colleagues, etc.  While you are not required to collaborate for the project, it will result in more of an interesting experience (plus extra credit).

Discuss your thoughts and interests and jot down **at least two** ideas for half-term projects that you could work on (either separately or together).  If you decide to work alone that is fine, but verbalizing your thoughts to others can help to solidify them!  

Some conversation starters:

* What are you interested in *outside of class*
* What would be interesting to *automate* or *sense* using a tiny device?
* Is there some sort of *experience* you could provide to others with your device?

Regardless, I want you **thinking** about your close-approaching future tasks!

# Resources

* Main lab resource: [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/playground-drum-machine](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/playground-drum-machine)
* Circuit Python Audio Out: [https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-audio-out](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-audio-out)

## Issues with audio files

If you have a `wav` file that doesn't work, ensure it is a 16-bit PCM @ 22KHz or less.  Here is a guide for how to use Audacity to convert them (and a relevant screenshot): [https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/check-your-files](https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/check-your-files)

<div align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/055/037/large1024/microcontrollers_downsample.png?1528215994" alt="downsample" />
</div>

## Full Code (in case if things went wrong and you just want to make some beats)

You'll need to tweak this for your individual files, however in case if you get stuck this can be used:

```
from time import sleep
import board
import neopixel
import gc
import digitalio
import touchio

from adafruit_waveform import sine

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

# Helper function to play a specified audio file
def play_file(filename):
    print("Playing file: " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)
    sleep(bpm / 960)  # Sixteenth note delay

# Setup audio variables
bpm = 120 
audio = AudioOut(board.SPEAKER)
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

# initialize neopixels
NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, brightness=0.05,auto_write=False)

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

# audio files played on touch - these files must exist
# on your CIRCUITPY drive in an audio folder!
audiofiles = ["./audio/bd_tek.wav",
              "./audio/elec_hi_snare.wav", 
              "./audio/elec_cymbal.wav",
              "./audio/elec_blip2.wav", 
              "./audio/bd_zome.wav", 
              "./audio/bass_hit_c.wav",
              "./audio/drum_cowbell.wav"]
              
# handy list to make iterating over touch inputs easy
touchPad = [touch_A1, touch_A2, touch_A3, touch_A4, touch_A5, touch_A6, touch_TX]

done = False
while not done:
    if btnA.value and btnB.value: # Both buttons pressed - exit
        done = True
    else:
        if btnA.value and btn_timer == 0:
            btn_timer = BTN_TIMER_DELAY

            sine_sample = RawSample(sine.sine_wave(220, 80))
            audio.play(sine_sample, loop=True)
            sleep(.5)
            audio.stop()
 
        if btnB.value and btn_timer == 0:
            btn_timer = BTN_TIMER_DELAY

            sine_sample = RawSample(sine.sine_wave(440, 40))
            audio.play(sine_sample, loop=True)
            sleep(.5)
            audio.stop()

    for i in range(len(touchPad)):
        if touchPad[i].value:
            play_file(audiofiles[i])

    # Handle button cooldown
    if btn_timer > 0: btn_timer -= 1

    pixels.show()
    sleep(.01)
    gc.collect()


print("Program done - exiting.")
```
