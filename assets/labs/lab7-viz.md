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

# Lab 6 - Visualizing Sensor Data

Last week you shared data with Bluetooth.  Now let's share it with serial.

Let's also up the complexity and hop languages - today you'll be writing both Circuit Python and JavaScript.

![oh no](https://i.pinimg.com/originals/c6/74/d1/c674d1952760d84034211fe15c081a80.gif)

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Data being sent from your Bluefruit to your p5js sketch

## Make your backup

We're going to be "starting fresh" again, though I'm going to get you some boilerplate sensor code.  We're not going to worry about min/max levels this time around.

So, backup last week's code as `code.lab5.py` and create a new `code.py` file.

## Getting started

We're going to transmit data over serial (i.e., what you print to the console in your Mu editor) and send it to a p5js sketch.

## p5js?

This is effectively a teaching tool for programming/JavaScript and is quite often used for making art.  I like it because it abstracts a lot of the difficult HTML5 canvas drawing calls, but the disadvantage is that it can be *slow* if you're rendering a lot of things.

Nice though for less memory-intensive applications!

{: .note }
They also have an excellent [reference guide](https://p5js.org/reference/) and set of [examples](https://p5js.org/examples/) and [tutorials](https://p5js.org/tutorials/) if you want to explore more.

Make sure you sign up for an account - you get cloud storage as part of it and you can easily access/share/edit your projects across devices.  

## Sending data from the Circuit Playground

Honestly, this is the easy part.  All you have to do is consider that whatever you `print` will be sent to your p5js sketch (so, avoid logging or trace debugging).

For instance, if I wanted to send both temperature and light, I could package that up as:

```python
# note - this is just an example
print(f"{temp_value},{light_value}".encode("utf-8"))
```

This would send a comma-separated string over serial to whoever is listening - your serial console, a p5js sketch, etc.  **It would be then up to the receiver to parse out that information!**

So, let's send out temperature, light, and our [accelerometer](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration) data (the acceleromater is something we'll be playing with later).

{: .note }
As a reminder, the `adafruit_circuitplayground` library tends to conflict with the `board` library - so choose one or the other when doing your projects.  This time we're using the former to make it easier to read data, but the `board` library is far more useful (to me, anyway).

```python
from time import sleep
from adafruit_circuitplayground import cp

while True:
  # get sensor values
  x, y, z = cp.acceleration
  temp_value = cp.temperature
  light_value = cp.light

  # print to serial
  print(f"{temp_value},{light_value},{x},{y},{z}".encode("utf-8"))
  
  # 😴
  sleep(0.5)
```

If you run this and check your serial console you should see a bunch of data.  Neato and a lot less steps than before.

The fun part is that is all we need from our device.  You'll extend it, naturally, but the basics are here.

## Receiving data in p5js

Clone the following sketch
Look up your serial connection

TODO

## What you should be seeing

# Homework extensions


# References

* [Adafruit Circuit Playground library](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express)
* [Sample p5js sketch using serial connection](https://editor.p5js.org/jps723/sketches/Byvw1lu6Z)