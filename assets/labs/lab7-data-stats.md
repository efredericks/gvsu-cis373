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

# Lab 7 - What do we do with our data?

Thus far we have (1) monitored data, (2) shared data, (3) stored data, but we haven't really talked about (4) what we do with our data!  Today we're going to be setting up our Circuit Playgrounds to monitor data, send it over UART to a Python program on our computers, and then perform some basic analyses. 

If you have a statistics background then you'll feel right at home.  If not, this is your future in either management or data analysis.

{: .warning }
This will involve using Python on **your computer**.  Make sure that you have a current version of Python and the `pip` installer setup!

<div align="center">
  <img src="https://pbs.twimg.com/media/EVTcWRJXsAAMC8K.jpg" alt="surprise" title="surprise" />
</div>

## Lab signoff

{: .warning } 

Before you leave for the day, (minimally) show me:

* Data being transerred to your computer
* A boxplot of temperature readings

## Getting started

1. Ensure you have a recent version of Python installed **on your computer** -- [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Ensure you have the Python package installer installed: [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

## Sending data from the Circuit Playground

Honestly, this is the easy part.  We are treating our device as a **sensor mote** that only sends data along.  All you have to do is consider that whatever you `print` will be sent to your python script (so, avoid logging or trace debugging).

For instance, if I wanted to send both temperature and light, I could package that up as:

```python
# note - this is just an example
print(f"{temp_value},{light_value}")
```

This would send a comma-separated string over serial to whoever is listening - your serial console, another device, a p5js sketch, etc.  **It would be then up to the receiver to parse out that information!**

So, let's send out temperature, light, and our [accelerometer](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration) data (the acceleromater is something we'll be playing with in the future, but I wanted you to see it now in case if you were using it in your term projects).

{: .important }
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
  print(f"{temp_value},{light_value},{x},{y},{z}")
  
  # 😴
  sleep(0.5)
```

If you run this and check your serial console you should see a bunch of data.  Neato and a lot less steps than before.

The fun part is that is all we need from our device.  You'll extend it, naturally, but the basics are here.

{: .warning }
Now that you're happy with your sending -- SHUT OFF THE SERIAL CONSOLE!  (In Mu you should be able to toggle it off or, better yet, close Mu altogether).  If you have a serial console running while you are trying to read/send data over that connection in a separate program you will *most likely* get a resource conflict and one of the two won't work!

## Receiving data via serial UART

Now, we need to receive data on our devices.  Today we'll use the USB connection instead of Bluetooth.

First, create a new folder to hold your project (we'll be setting up a virtual environment so everything is self-contained).  

Call it `yourlastname-lab7` (replacing `yourlastname`, obvs).

Inside that folder create a Python script `yourlastname-lab7.py`.

If I were doing this it would look like:

``` bash
+ fredericks-lab7/
    * fredericks-lab7.py
```

### Setting up a virtual environment

First, we'll setup a virtual environment.  While it isn't strictly necessary, a virtual environment can prevent your system from being polluted with conflicting Python package versions.

Navigate to your lab7 folder in your terminal and create one:

`python3 -m venv venv`

``` bash
+ fredericks-lab7/
    * fredericks-lab7.py
    * venv/
```

You should now have a folder called `venv` in that directory.  It will hold (among other things) startup scripts, a version of Python, and a place to hold all your Python packages.

To use it (in Linux/Mac) you can run:

`source venv/bin/activate` (from your lab directory).

{: .important }
I am using Linux to do this and don't have a Windows machine to try it out on.  If you're using PowerShell then this *may* work: `Scripts\activate.ps1`.  Check the [`venv` documentation](https://docs.python.org/3/library/venv.html) for PowerShell-specific instructions.


You should now see something like this in your terminal, this means that all your Python commands are working within the virtual environment instead of your global system.  All packages you install will be installed to the `venv` directory.

```bash
erik@worktop:~/fredericks-lab7$ source venv/bin/activate
(venv) erik@worktop:~/fredericks-lab7$
```

To exit your virtual environment, you can either exit the terminal or type `deactivate`.

### Installing libraries

To do our data analyses we'll be using the `scipy` library and plotting it with `seaborn`.  `scipy` has a **ton** of functionalities and I encourage you to check it out.  `seaborn` is essentially `matplotlib` but with prettier visuals.

We also need the `pySerial` library to parse out the UART serial information.

```bash
python3 -m pip install scipy
python3 -m pip install seaborn
python3 -m pip install pyserial
```

After the install occurs, you can test it by entering Python directly:

```bash
$ python3
>>> import scipy
>>> import seaborn
>>> import pyserial
```

If you see errors with any of those imports then you have an installation issue.  **Fix them before you move on**.

## Receiving data 

Edit your Python script on your computer (the `yourlastname-lab7.py` script):

{: .important }
The path to the serial port is different between devices.  If you are on Linux it is most likely `/dev/ttyACM0`, on Windows it will be one of your COM ports such as `COM3`, and on Mac it will be something like `/dev/cu.usbmodem14101`.
You discover it by (1) knowing where to look on your computer and (2) watching that directory when you plug in your device -- the 'new' device will be your Circuit Playground!

Fortunately, the `pySerial` library can auto-detect our port.  However, if you look for other serial scripts typically the serial port will be hard coded.

```python
import serial
import serial.tools.list_ports
import time

# discover circuit playground serial port
def find_circuit_playground():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == 0x239A:  # Adafruit vendor ID
            return port.device
    return None

port = find_circuit_playground()
if port is None:
    print("Error finding device - use a direct variable to your port instead")
    exit

# configure serial connection
uart = serial.Serial(port, baudrate=9600, timeout=10) 

# wait for device to be ready then flush startup messages
# otherwise we get a weird byte from the initial boot startup
time.sleep(2)
uart.flushInput()

while True:
    # read data
    data = uart.readline() 
    if data: 
        parsed_data = data.strip().decode("utf-8")
        print(parsed_data)

    time.sleep(0.1)
```

If you run your Python script on your computer **and** your Circuit Playground is plugged in then you should see some data flowing:

```bash
23.5778,7,7.77585,-4.74978,3.98369
23.5996,7,7.62263,-4.74978,4.0603
23.5123,7,7.58433,-4.74978,4.02199
23.5778,7,7.81416,-4.78809,4.0603
23.5123,7,7.69924,-4.71148,4.25182
```

If you recall, your data format is comma-separated and is `temperature,light,acceleration X, acceleration Y, acceleration Z`.  Let's now parse that out.

Change your parsing statement:

```python
parsed_data = data.strip().decode("utf-8").split(',')
print(parsed_data, parsed_data[0])
```

You should now see an array printing - this also means you can access them individuall with `parsed_data[0]` and so on:

```bash
['23.6213', '7', '7.69924', '-4.63487', '4.21351'] 23.6213
['23.6213', '7', '7.73755', '-4.78809', '4.17521'] 23.6213
['23.5559', '7', '7.69924', '-4.59656', '4.55826'] 23.5559
['23.5778', '7', '7.73755', '-4.63487', '4.0986'] 23.5778
```

{: .important }
Note that these are still strings in the array!

## Plotting with seaborn

Let's do some basic temperature plotting.  *Gasp* - that's the signoff!

![italian spiderman](https://media.tenor.com/dZ1ZlOK7oksAAAAM/italian-spiderman-what.gif)

**Outside** of your main loop, create an array to store data with.

```python
temperatures = []
while True:
    ...
```

{: .note }
An enterprising, looking-ahead type of student might want to create similar arrays for all the other data we're parsing...

Now, get the temperature and add it to the array:

```python
    # after we parse our data...
    temperatures.append(float(parsed_data[0]))
```

Neat, we have an ever-expanding array.  This definitely won't be a memory problem in the near future...

**Change** your loop to monitor 50 messages:

```python
timeout = 50
while timeout > 0:
    ...
    timeout -= 1
    time.sleep(0.1)
```

## Simple analysis

Let's look at the minimum, maximum, and average temperature values.

At the bottom of your script (i.e., **after** your main loop) print a summary:

```python
# stats time
min_temp = min(temperatures)
max_temp = max(temperatures)
ave_temp = sum(temperatures) / len(temperatures)
print("::Temperature statistics::")
print(f"Min: {min_temp:.2f}, Max: {max_temp:.2f}, Average: {ave_temp:.2f}")
```

{: .note }
What happens if the temperatures list is empty?  Do we need to do something about that?

{: .warning }
Yes we do - fix it now:

```python
# stats time
if len(temperatures) > 0:
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    ave_temp = sum(temperatures) / len(temperatures)
    print("::Temperature statistics::")
    print(f"Min: {min_temp:.2f}, Max: {max_temp:.2f}, Average: {ave_temp:.2f}")
else:
    print("Error: temperatures list empty!")
```

Now, plot it! We'll first need to import the `seaborn` and `matplotlib` libraries -- at the top:

```python
import seaborn as sns
import matplotlib.pyplot as plt
```

Within your statistical analysis block:

```python
# plot
sns.boxplot(y=temperatures)
plt.title("Temperatures over 50 samples (finger off)")
plt.xlabel("Data")
plt.ylabel("Temperature (C)")
plt.show()
```

You should see a box plot with some relevant statistical information. Essentially, the whiskers indicate the minimum/maximum values in the dataset, the box itself shows the quartiles, and the line in the box shows the median.  Useful for visualizing datasets and comparing them!

Read more about box plots:
> * [https://www.atlassian.com/data/charts/box-plot-complete-guide](https://www.atlassian.com/data/charts/box-plot-complete-guide)
> * [https://www.geeksforgeeks.org/data-analysis/box-plot/](https://www.geeksforgeeks.org/data-analysis/box-plot/)

## Refactoring

Analyses are kind of bland without a point of comparison.  This is going to be a ham-fisted way of doing things, but we're going to add some basic user interaction to your local Python scripts to collect different types of data.

First, your forever loop is going to become a function and you'll return the sampled data.  Second, we'll do two passes where we monitor the temperature sensor alone and with your finger on it.

For example, pass 1 will record the 'standing' data and pass 2 will record you doing something to the device.  Meaning, let's compare you putting your finger onto the device vs. not.

Add a new function at the top:

```python
# record a pass of temperatures
def monitor_temperature(_timeout=50):
    _temperatures = []
    timeout = _timeout

    while timeout > 0:
        # read data
        data = uart.readline() 
        if data: 
            parsed_data = data.strip().decode("utf-8").split(',')
            _temperatures.append(float(parsed_data[0]))
        timeout -= 1
        time.sleep(0.1)
    return _temperatures
```

This simply takes your while loop code and moves it to a dedicated function.  That means we now need to refactor the main loop.  Comment out everything in your `while timeout > 0` loop and simply do (i.e., without the loop):

```python
print("Standalone temperature")
temperatures = monitor_temperature()
```

Your code should work the same (except you won't be printing anything in the loop).  **If it does not work then you have an error**.

Now, the fun part.  Do a secondary recording **with your finger on the temperature sensor**.

First, add a user interaction call to let you press enter to move on.  After your temperature recording:

```python
input("Put your finger on the temperature sensor and press enter")
user_temperatures = monitor_temperature()
```

You should now have two lists of data with the same number of data points.  Now, modify the analyses -- you should see two sets of statistics and two boxplots:

```python
# stats time
if len(temperatures) > 0 and len(user_temperatures) > 0:
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    ave_temp = sum(temperatures) / len(temperatures)

    min_user_temp = min(user_temperatures)
    max_user_temp = max(user_temperatures)
    ave_user_temp = sum(user_temperatures) / len(user_temperatures)

    print("::Standing temperature statistics::")
    print(f"Min: {min_temp:.2f}, Max: {max_temp:.2f}, Average: {ave_temp:.2f}")
    print("::User temperature statistics::")
    print(f"Min: {min_user_temp:.2f}, Max: {max_user_temp:.2f}, Average: {ave_user_temp:.2f}")

    # plot
    temperature_data = [temperatures, user_temperatures]
    sns.boxplot(data=temperature_data)
    plt.title("Temperatures over 50 samples")
    plt.xticks([0, 1], ['Standing', 'User pressed'])
    plt.xlabel("Data")
    plt.ylabel("Temperature (C)")
    plt.show()

```

{: .important }
Note the change from `y=` to `data=`!

> One thing with this form of analysis - we're somewhat "cheating" by only using Python lists. If you really want to perform powerful statistical analyses, consider learning about the `pandas` library.  This essentially allows you to do R in Python.

## Analysis with scipy

Neat, you have a box plot comparing data and some relevant stats.  However, are they different?  Are they the same?  The fun fact is:

<font style="font-size:3em">YOU DON'T KNOW</font>

If you know statistics you know they can easily lie or be misconstrued.  Even if boxplots look different they may be telling a different story.  That's a discussion for a stats course, however there's an easy way we can tell.  

Without going further down the rabbit hole we can analyze our data with a statistics package.  As long as our data sets have the same amount of data we can analyze their similarity with a *test*.  We'll be using the *Wilcoxon-Mann-Whitney u-test*.

> Note, there are *many* different types of tests and they each depend on the shape and distribution of your data.  Ours assumes that the numbers have the same distribution: [https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test).  We enforce that by having the same number of data points and use the same type of values.  If you try comparing your light values to your temperature values, for instance, this distribution is broken and your test is invalid!

At the top, import `scipy`:

```python
from scipy.stats import wilcoxon
```

and below your plots, add the statistical test (note that they won't appear until you close the plot because it blocks program execution):

```python
statistic, pvalue = wilcoxon(temperatures, user_temperatures)
print(f"P-value: {pvalue}")
```

We're looking for a *p-value < 0.001* to indicate a **significant difference**, otherwise we can't say if one dataset is different from another!

Your p-value should be pretty tiny.  Try it again without putting your finger on the second stage!

{: .note }
You may still notice a significant difference even without your input.  This could be due to the fact that we're taking a tiny number of samples (50 isn't that much) or that our temperature sensor is a bit 'jumpy.'  If so, try increasing the number of samples to 500 to see if a larger range helps! You can also reduce the delay in your Circuit Playground's `code.py` as well to make it speed up a bit.

> Remember, the number of samples can be passed into the `monitor_temperature` function!  

{: .note }
If you still see significant differences then it is most likely that we'd need to average the temperature over multiple runs.  Our values are just too jumpy.  The solution is in the extra credit!

## Homework extensions

1. Do the same process for the light values -- provide the min/max/average statistics, a box plot comparison standalone vs. user interacted (i.e., you covered the light), and your *p-value*.

2. Do some additional research - one thing with this type of test is that you formulate a null hypothesis and an alternate hypothesis.  **In your own words**, what are these and how does the *p-value* influence them?  Make sure you cite your source(s) for this one - an LLM does not count.

3. We have a set of results.  Assume you are a manager of a team that has deployed a sensor network of Circuit Playgrounds with the capabilities you've done so far.  What are **two** actionable items (meaning, decisions) you could make with the data summaries?  Provide some detail, not just a bullet point or a weak phrase.

4. Make progress on one aspect of your term project and demonstrate that you did it.

## Extra credit opportunity!

We directly sampled the sensors and calculated the statistics.  Do the same process, but instead sample the device 10 times, average those values, then add the average to a list.  Do that 50 times (so, 50 averages in a list meaning you've sampled the device 500 times in total).  Do the same for the user-pressed section, and then do the same comparison.  

Do the values appear different?  What happens if you leave your finger off?  Provide a short report of this experiment.