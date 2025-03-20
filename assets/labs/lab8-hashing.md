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

This week we're going to keep it simple.  We're going to encrypt some data, clean up our debouncing, and then make our device mildly more secure than it was before.

For this, we're going to make use the `hashlib` library.  Note that if we were to be setting up secured communications then you'd need to be manually-coding a handshake to properly secure things.  This little library is only going to take us so far.

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Your device outputting an encrypted string.

## Make your backup

We're going to be "starting fresh."  So, backup last week's code and create a new `code.py` file.

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

### SECRETS

One other thing that may be useful is to learn about the secrets or settings file.  This is a special file typically used to abstract away things like passwords, API keys, etc.

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

# add buttons
...

done = False
while not done:
    # Update our debouncers
    btnA_debounced.update()
    btnB_debounced.update()

    ...

```

{: .note }
We can use `btnA_debounced.value` to check the button state, however you'll probably see it double-triggering.  Not ideal!  Either use `btnA_debounced.fell` to detect if the button is pressed or `btnA_debounced.rose` to detect if the button is released.

## Putting it together

We can encrypt/decrypt information and we can save important information to separate files.  Let's now put it together.





-----------------

Your job for the homework (as specified below), is to store a string on your device, encrypt it with MD5, receive a string from UART (i.e., sending the string from Bluetooth Connect to your device), and then checking if it was valid or not. 

As a hint, you'll need to create a second hash object to handle the incoming string.

## Homework - Hashing and unlocking

Your device must be unlockable through a key combination, and the comparison must use the `md5` function to compare (similar how you would with a password).

1. Store the letter combination in your `settings.toml` file - it should be `ABAABBA`.
2. If the device is locked, then the LED ring should be red.  If the device is unlocked, the LED ring should be green.
3. When the device is unlocked, print the current temperature value to the serial console.  When it is locked, print nothing.

# References

* [CircuitPython Hashlib](https://docs.circuitpython.org/projects/hashlib/en/latest/)
* [Simple hashlib example (various forms of hashing)](https://docs.circuitpython.org/projects/hashlib/en/latest/examples.html)
* [CircuitPython settings file](https://learn.adafruit.com/mqtt-in-circuitpython/create-your-settings-toml-file)