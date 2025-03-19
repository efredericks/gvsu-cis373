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

This week we're going to keep it simple.  Let's encrypt and decrypt some data since security is a concern for us as well, in addition to things like sensing, logging, etc.

For this, we're going to make use the `hashlib` library.  Note that if we were to be setting up secured communications then you'd need to be manually-coding a handshake to properly secure things.  This little library is only going to take us so far.

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Your device taking a string and outputting its encrypted format.

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

Your homework will have you using the `adafruit_hashlib` library to encrypt data (and compare hashed data).  The workflow will be to have a secret password on your local device and hash it.  Your phone (over the Bluetooth Connect app) will send a string and you will compare the hashed value.  

Kind of like how usernames/passwords are handled in some websites.  The password is stored hashed (**NEVER PLAINTEXT**) and compared with a hash of the user's input.

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

### SECRETS

One other thing that may be useful is to learn about the secrets file.  This is a special file typically used to abstract away things like passwords, API keys, etc.

{: .warning }
If you are using source control (e.g., GitHub), DO NOT check your `settings.toml` or `secrets.py` file in with your actual information!  Make sure you delete it before pushing.

The format is pretty straightforward - create an empty file called `settings.toml`.

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

You should see both variables printing to your console.  

## Debouncing with a library

Previously we debounced manually.  There is a [library we can use](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing) to make it a bit cleaner.

Copy over the `adafruit_ticks.mpy` and `adafruit_debouncer.mpy` library files onto your device's `lib` folder.

## Putting it together

We can encrypt/decrypt information and we can save important information to separate files.  Let's now put it together.





-----------------

Your job for the homework (as specified below), is to store a string on your device, encrypt it with MD5, receive a string from UART (i.e., sending the string from Bluetooth Connect to your device), and then checking if it was valid or not. 

As a hint, you'll need to create a second hash object to handle the incoming string.

## Homework - Hashing data

For your deliverables, your code must do two things:

1. `code.yourlastname.beacon.py`: Broadcast accelerometer data, temperature data (from the sensor, NOT the CPU), and light data.  I will be testing with the same node that we had in the lab, so I will be looking at my Serial output for your data.  

2. `code.yourlastname.hash.py`: Receive a string over Bluetooth UART, hash it using `MD5`, and compare it to a known key.  Your program should print to the Serial console that a received string was either valid or invalid, and that comparison **must** be using the hashed values, not plaintext!

The key you need to encrypt is:

> CIS373 is fun

You will submit **two separate code files** for this lab to avoid having the Bluetooth elements conflict with each other.  Name the first one `code.yourlastname.beacon.py` and the second `code.yourlastname.hash.py`.

## Want extra credit? 

Two options here - IN YOUR REPORT LET ME KNOW WHAT YOU DID SO I CAN CHECK IT!

1. Include other data within the packet.  Acceleration, light, and temperature are the minimum required.  Additional points for every extra "valid" data included (including custom data).

2. Have your LEDs react to the received string.  If it is invalid, show red.  If it is valid, show green.  Note, since we're using `adafruit_circuitplayground` you will have to handle LEDs differently - it is up to you to lookup how [+15].

3. Set your device up to re-broadcast data from other nodes (essentially, flooding). [+30].  If you do this, tell me what I need to do for sending data to your device as well as receiving.

# References

* [Adafruit BLE broadcastnet](https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/examples.html)
* [Adafruit BLE broadcatnet API](https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/api.html)
* [Adafruit CircuitPlayground Library reference](https://docs.circuitpython.org/projects/circuitplayground/en/latest/examples.html)
* [Adafruit Acceleration](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration)
* [CircuitPython Hashlib](https://docs.circuitpython.org/projects/hashlib/en/latest/)
* [Simple hashlib example (various forms of hashing)](https://docs.circuitpython.org/projects/hashlib/en/latest/examples.html)
* [What is a Beacon?](https://kontakt.io/blog/what-is-a-beacon/)