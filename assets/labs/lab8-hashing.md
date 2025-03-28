---
layout: page
title: Lab 8
nav_exclude: True
description: >-
    Lab 8 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 8 - Hashing Sensor Data!

{: .warning }
Since there are differences with the Express and Bluefruit in terms of available memory we're going to be **skipping** the hashing part for the homework (i.e., the Express doesn't seem to be able to load in `adafruit_hashlib`).  You are still welcome to do it but it is no longer required.

This week we're going to keep it simple.  We're going to encrypt some data, clean up our debouncing, and then make our device mildly more secure than it was before.

For this, we're going to make use the `hashlib` library.  Note that if we were to be setting up secured communications then you'd need to be manually-coding a handshake to properly secure things.  This little library is only going to take us so far.

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Your device outputting an encrypted string.

## Make your backup

We're going to be "starting fresh."  So, backup last week's code and create a new `code.py` file.  You can also remove the `boot.py` file since we won't be writing to disk this lab (and we don't want it messing anything up).  After you do make sure you do a full power reset of the device!

{: .note }
If you have a Bluefruit and are interested in Bluetooth beacons, [last year's lab](/assets/labs/prior/lab8.md) provides information on that.  The documentation is a bit circuitous, so this might be helpful.

## A quick aside

I've noticed one of my Bluefruits would randomly soft-reboot itself quite often, and it was annoying.  This is the solution if it happens to you, care of Adafruit ([https://learn.adafruit.com/adafruit-circuit-playground-express/troubleshooting](https://learn.adafruit.com/adafruit-circuit-playground-express/troubleshooting)):

```python
import supervisor
supervisor.runtime.autoreload = False
```

## Getting started

First, add the following library to your devices:

1. `adafruit_hashlib`

## Hashing and handshaking

You'll eventually be locking/unlocking your device via a secret keycode.  Typically you would never store anything in plaintext and only store the hashed values.  For simplicity's sake we'll be storing a plaintext password in this lab, however a better approach is to hash it and then store it.

### Basic hashing

As mentioned we'll use `adafruit_hashlib` for our encryption.  Import it!  Note, the following code is a snippet from the hashlib documentation:

```python
import adafruit_hashlib as hashlib

# Create an MD5 message
print("--MD5--")
byte_string = b"CircuitPython"
m = hashlib.md5()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
```

So what you should get out of that block of code is that you need (1) a string to encrypt, a specific encryption algorithm to run (in this case, MD5), and a way to access the output (for us, in `m.hexdigest()`).

We now have a way to hash a string.  MD5 is pretty common, however there are a large number of other hashing techniques out there.

Lets do a simple test.  Add a password and "check" (the assumption would be that we receive it from somewhere else) to see if it is the same or not:

```python
password = "Temp12345"
user_input  = "temp12345"

m1 = hashlib.md5()
m1.update(password)

m2 = hashlib.md5()
m2.update(user_input)

print(m1.hexdigest(), m2.hexdigest(), m1.hexdigest() == m2.hexdigest())
```

And, if you change the `user_input` to be correct, you should see the comparison be `True`.

### SECRETS

One other thing that may be useful is to learn about the secrets or settings file.  This is a special file typically used to abstract away things like passwords, API keys, etc.  It used to be `secrets.py` and has transitioned over to `settings.toml`.

{: .warning }
If you are using source control (e.g., GitHub), DO NOT check your `settings.toml` or `secrets.py` file in with your actual information!  Make sure you delete the saved password information before pushing.

The format is pretty straightforward - create an empty file called `settings.toml`.  Values saved here will be stored to your environment variables local to your Python program.

```python
test="Hello world"
thumbsup="👍"
```

Here is more information on this approach - note the link itself is for MQTT (and setting things up like WiFi), so there's a bit more info there: [https://learn.adafruit.com/mqtt-in-circuitpython/create-your-settings-toml-file](https://learn.adafruit.com/mqtt-in-circuitpython/create-your-settings-toml-file)

And in your `code.py` file:

```python
import os

print(os.getenv("test"))
print(os.getenv("thumbsup"))
```

You should see both variables printing to your console.  If you wanted to, say, save one of those variables to be used within your program all you'd have to do is:

```python
myvar = os.getenv("test")
```

Ok, so now we have:

1. The ability to hash a string
2. The ability to save 'important' information to a separate file.

{: .note }
Support for the `settings.toml` file only started with CircuitPython 8!

Let's go ahead and "do better" with button debouncing, since we'll be relying on button presses to log in to our devices.

## Debouncing with a library

Previously we debounced manually.  There is a [library we can use](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing) to make it a bit cleaner.

Copy over the `adafruit_ticks.mpy` and `adafruit_debouncer.mpy` library files onto your device's `lib` folder (`debouncer` depends on `ticks`).

Instead of mucking about with timers and trying to get the feel "just right" we'll use the debouncer library with button states instead.  It'll be a little bit cleaner, plus you can still play with delays to dial in the feel if you wish.

{: .note }
The "feel" is handled with the `interval` value mentioned below.

Import `adafruit_debouncer` and create your buttons as usual.  However, we're going to add a debounced object and update the value each iteration.

```python

from adafruit_debouncer import Debouncer

# create the md5 object
...

# setup buttons
btnA = digitalio.DigitalInOut(board.BUTTON_A)
btnA.switch_to_input(pull=digitalio.Pull.DOWN)

btnB = digitalio.DigitalInOut(board.BUTTON_B)
btnB.switch_to_input(pull=digitalio.Pull.DOWN)

btnA_debounced = Debouncer(btnA)
btnB_debounced = Debouncer(btnB) # Debouncer(btnB, interval=0.05) 

done = False
while not done:
    # Update our debouncers
    btnA_debounced.update()
    btnB_debounced.update()

    if btnA_debounced.value and btnB_debounced.value: # Both buttons pressed - exit
        done = True
    else:
        if btnA_debounced.rose:
            print("Button A released")

        if btnB_debounced.rose:
            print("Button B released")

    ...
```

{: .note }
We can use `btnA_debounced.value` to check the button state, however you'll probably see it double-triggering.  Not ideal!  Either use `btnA_debounced.fell` to detect if the button is pressed or `btnA_debounced.rose` to detect if the button is released.

## Putting it together

We have done a few things that seemingly are random.  Let's put them together.  Let's make our device unlockable!

At the top, define two new variables:

```python
unlock_code = "ABAB"  # our password
user_code = ""        # the user's entry
```

Then, any time the A or B buttons are pressed, add on a new character to the user variable.  It will also be helpful to print out the current state to the terminal for debugging.  For instance on Button A's release:

```python
if btnA_debounced.rose:
    user_code += "A"

# btnB handling

print(user_code)
```

Now, "unlock" the device!  Check if `user_code` matches `unlock_code` and print when the device is unlocked.

## Homework - Hashing and unlocking

Your device must be unlockable through a key combination, and the comparison must use the `md5` function to compare (similar how you would with a password).

1. Store the letter combination in your `settings.toml` file - it should be `ABAABBA`.  
2. The device can only be unlocked if the <del>*hashed* version of the</del> letter combination matches the <del>*hashed* version of the</del> user input.  
3. If the device is locked, then the LED ring should be red.  If the device is unlocked, the LED ring should be green.
4. When the device is unlocked, print the current temperature value to the serial console.  When it is locked, print nothing.
5. When buttons A and B are pressed at the same time, reset the current key combination instead of ending the program.

# References

* [CircuitPython Hashlib](https://docs.circuitpython.org/projects/hashlib/en/latest/)
* [Simple hashlib example (various forms of hashing)](https://docs.circuitpython.org/projects/hashlib/en/latest/examples.html)
* [CircuitPython settings file](https://learn.adafruit.com/mqtt-in-circuitpython/create-your-settings-toml-file)
