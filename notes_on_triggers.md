# Notes on making triggers for EEG and TMS
In short, to send triggers to EEG to mark events in the task or to the TMS to trigger stimulation, you need to send a code from your stimulus presentation software (PyschoPy, etc.) to the hardware.

See the example code for suggestion on how to define triggers in PsychoPy scripts [here](https://github.com/CoInAct-group/Experimental_Methods/blob/main/EEG/eeg_trigger_tutorial.py).

## 1) Serial and parallel ports
The most common way to send a trigger is though a parallel port or a serial or USB port. 

Parallel ports sends values based on parallel "pins" that each represents a bit in a binary number. For example with eight pins, you can write values from 0-255. Parallel ports are generally the most reliable way of sending triggers as all information is send at the same time. However, modern PCs and laptops do not have parallel ports.

Serial ports can send different values where the information is send in series of "packages". This means that the timing and how the codes are read at the reciving end can be off if not handled correctly. Serial ports can be used to emulate parallel ports if given only length 1 and proper encoding.

This example takes the integer `code` and transformes it to a code that can be send over serial to emulate a parallel trigger (not that it only works for numbers 0-255):

````python
code.to_bytes(1, 'big')
````

## 2) Use win.callOnFlip() to time triggers in PsychoPy
PsychoPy has a build-in method that is supposed to control the timing in how it executes functions to deliver stimuli related to the ``Window`` module called `callOnFlip()`. The method takes a function and the input to the function as arguments and will call the function immediately after the next flip() command. If this the next `flip()` is when the visual stimuli is drawn, the should be function will be executed when the stimuli is drawn.

The first argument should be the function to call, the following args should be used exactly as you would for your normal call to the function (can use ordered arguments or keyword arguments as normal):  ``callOnFlip(function, *args, **kwargs)``

E.g. If you have a function that you would normally call like this (code is the trigger value):

````python
port.write(code.to_bytes(1, 'big'))
````
You call it though ``callOnFlip()`` like this:

```python
win.callOnFlip(port.write, code.to_bytes(1, 'big')) 
```

## 3) Find the USB serial port address
Plug in the USB cable connected to the EEG system or TMS.

### Windows
On most Windows machines the serial port is callel "COM" and a number, e.g., "COM3". The exact name vary from machine to machine. Open the Device Manager (from the menu). Go to the overview of USB devices. Find the one corresponding to the connected device. Somewhere in the name it (sometimes) list the COM name.

If not, you can always do a "brute force" test, and see if you get triggers with any adresses, starting with "COM1", "COM2", and so on.

### Mac
On Mac, USB ports are found under devices and called "tty.<something>. To find the name, open a terminal and type:
```bash
ls /dev/tty.*
```
Then find the name that match the connected device.

This adress usually works: 

````python
port = serial.Serial('/dev/tty.usbserial-DN2Q03LO', 115200)
````