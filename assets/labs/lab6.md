---
layout: page
title: Lab 6
nav_exclude: True
description: >-
    Lab 6 page.
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# Lab 6 - Sharing Sensor Data!

This week we're going to keep it simple.  Let's share some data.  We're going to send sensor data from your devices to a central node (so essentially single-hop flooding).  You're going to measure sensor data and broadcast it to the  network. 

A central node (me) will be setup to receive that data.  You will setup your devices as beacons to send it out.  Consider yourselves motes in a large sensor network.

We're also going to do some encryption and decryption since security is a concern for us as well (though that will be homework for you and the topic of a future lecture).

However, the libraries available for our devices are significantly limited in terms of handshakes (hence why there was no security when we were broadcasting our sensor readings).  So, we're going to make do with the `hashlib` library.

{: .note } 
Essentially, you would need to manually code a handshake prior to sending/receiving data if you wanted a properly-secured environment.


## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Your Bluefruit broadcasting CPU temperature over Bluetooth. 

## Make your backup

We're going to be "starting fresh" and creating two separate scripts.  So, backup last week's code and create a new `code.py` file.

## Getting started

First, add the following libraries to your devices:

1. `adafruit_ble_broadcastnet`
2. `adafruit_circuitplayground`
3. `adafruit_hashlib`

## First, what are beacons?

A [beacon](https://kontakt.io/blog/what-is-a-beacon/) is a sensor node that makes a controlling node aware of local data (essentially, a mote that broadcasts some measured value or checks to see if another node is in range).  We'll use the `adafruit_ble_broadcastnet` library to allow our devices to act as beacons.  Note that the transmission code is a bit different than prior Bluetooth connection labs - here we want to blast data out and don't particularly care who receives it.

{: .note }
Consider: this is the "dumb" method of sending out data.  What would we need to do to make it more intelligent?  For instance, forwarding received data from other nodes?

<div align="center">
  <img src="https://www.minew.com/product/beacon-sensor/beacon_files/1-1.jpg" alt="beacon ad" />
</div>

### Basic broadcasting

We're going to slightly change things up and use the `adafruit_circuitplayground` library to access sensor data.  One it will give you a different library to try out, and two it will make reading accelerometer data a heck of a lot easier.

{: .warning }
Your old code for reading the `board` and `NeoPixels` will not work with this lab.  You will need to use the `adafruit_circuitplayground` library for handling those types of things!

This code is slightly modified from here: [https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/examples.html](https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/examples.html)

```
import time
import microcontroller
import adafruit_ble_broadcastnet
from adafruit_circuitplayground import cp
import gc

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

while True:
    # Create measurement object, assign temperature, and then broadcast it
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    measurement.temperature = (
        microcontroller.cpu.temperature  # pylint: disable=no-member
    )
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement, broadcast_time = 1)

    gc.collect()
    time.sleep(2)
```

This code will retrieve the CPU temperature, package it into an `AdafruitSensorMeaurement` object, and then send it over BLE broadcast.  Check out this page for a reference of all the different types of measurements you can send: [https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/api.html](https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/api.html).

{: .note }
Also consider: what if we want to use a "non-standard" reading?  What if we wanted to send a string? 

### Testing your outputs

Note: testing this will be tricky as the Bluefruit app *will not work* for generic Bluetooth broadcasts.  You have two options for testing: check with me and my "sink node" to make sure data is going through (highly-recommended before you leave or during office hours), or check your Serial output for a measurement object.

Your output should look like this (note the readings for temperature, acceleration, and light included within the packet):

```
This is BroadcastNet sensor: e8318f349bbc
<AdafruitSensorMeasurement temperature=35.267 acceleration=mdf_tuple(x=-0.191523, y=0.114914, z=9.46126) light=316.0 sequence_number=0 >
```

### The deliverables

You see how you can send data over broadcast.  Any device that knows how to read a BLE broadcast can pick up this message.

For the homework, add the following readings (this will involve checking the `Adafruit_CircuitPlayground` API to know how to get those values and creating `measurement` attributes on the `AdafruitSensorMeaurement` object you created).  The links are at the bottom of this page for both of these objects.

* **Replace CPU temperature with air temperature**

* **Add the current light value**

* **Add the x, y, and z accelerometer readings**

(To save you some headache, here is how you access the accelerometer - you will need to create a tuple object to assign it to the `acceleration` property):

```
x, y, z = cp.acceleration
```

## Hashing and handshaking

Your homework will have you using the `adafruit_hashlib` library to encrypt data (and compare hashed data).  The workflow will be to have a secret password on your local device and hash it.  Your phone (over the Bluetooth Connect app) will send a string and you will compare the hashed value.  

Kind of like how usernames/passwords are handled in some websites.  The password is stored hashed (**NEVER PLAINTEXT**) and compared with a hash of the user's input.

### Bluetooth boilerplate

To help you out with the Bluetooth connections (there were some growing pains the last time we did this), here is a bit of boilerplate to get you started.  What happens here is that the code waits for a Bluetooth connection, then starts running forever, however will only do things if a Bluetooth connection is active within that loop (for instance, we don't want to be handling data if the connection was dropped...).

{: .note }
Ensure you rename your previous `code.py` file to `code.yourlastname.beacon.py` (you'll be submitting it separately).

```
import adafruit_hashlib as hashlib
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import time
import gc

# Create Bluetooth objects
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.name = "yourlastname-BlueFruit"

# Advertise and wait for connection
ble.start_advertising(advertisement)
print("Waiting to connect")
while not ble.connected:
    pass
print("Connected")

# Forever loop
while True:
    # only do things with bluetooth if connected
    if ble.connected:
        line = uart.readline()  # receive data from UART
        line = line.strip()     # remove trailing newline
        print(line)

    gc.collect()
    time.sleep(0.5)
```

### Basic hashing

As mentioned we'll use `adafruit_hashlib` for our encryption.  Import it!  Note, the following code is a snippet from the hashlib documentation:

```
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

Your job for the homework (as specified below), is to store a string on your device, encrypt it with MD5, receive a string from UART (i.e., sending the string from Bluetooth Connect to your device), and then checking if it was valid or not. 

As a hint, you'll need to create a second hash object to handle the incoming string.

Here's a video of what I'd expect to see: TBD - RECORD VIDYA



## Homework - Hashing data

For your deliverables, your code must do two things:

1. `code.yourlastname.beacon.py`: Broadcast accelerometer data, temperature data (from the sensor, NOT the CPU), and light data.  I will be testing with the same node that we had in the lab, so I will be looking at my Serial output for your data.  

2. `code.yourlastname.hash.py`: Receive a string over Bluetooth UART, hash it using `MD5`, and compare it to a known key.  Your program should print to the Serial console that a received string was either valid or invalid, and that comparison **must** be using the hashed values, not plaintext!

The key you need to encrypt is:

> CIS373 is fun and I am not being coerced into saying that as part of a deliverable

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


-----------------------

import adafruit_hashlib as hashlib
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import time

#m = hashlib.sha256()
#m.update(b"CircuitPython")

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


ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.name = "Fredericks-BlueFruit"

print("Msg Hex Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size))

ble.start_advertising(advertisement)
print("Waiting to connect")
while not ble.connected:
        pass
print("Connected")

while True:
    if ble.connected:
        line = uart.readline()
        line = line.strip()
        m2 = hashlib.md5()
        m2.update(line)
        print(line, m2.hexdigest())
        
        if (m.hexdigest() == m2.hexdigest()):
            print("YOU WIN")
            break
    time.sleep(0.5)

HW: make LEDs light up green when password is sent, red if failed

Q's: what is a sequence number?  
what is broadcast_time?
Why is flooding a possible issue in sensor nets?
What kind of data does the accelerometer provide?


==REMOVE ME==
21 - sensor net lab
28 - accelerometer + security lab?
4 - work on term project
11 - work on term project
18 - presentations

IoT:

Get sensor measurements setup
Install BLE broadcastnet
broadcast 2 sensor readings (prepend name to value)
extra credit - pick up a friend's reading and rebroadcast -- make a handshake to "login" to your device
==REMOVE ME==

accel
https://docs.circuitpython.org/projects/ble_broadcastnet/en/latest/api.html
https://learn.adafruit.com/bluetooth-le-broadcastnet-sensor-node-raspberry-pi-wifi-bridge/install-pi-bridge-software
https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet/blob/main/examples/ble_broadcastnet_blinka_bridge.py

battery broadcast: https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet/blob/main/examples/ble_broadcastnet_battery_level.py

hashlib: https://github.com/adafruit/Adafruit_CircuitPython_hashlib

