# -*- coding: utf-8 -*-
"""
Created on Thur 6 March 11:19:42 2025
@author: cqw485

This script sends triggers to a parallel port (USB) with jittered Inter-Stimulus Intervals (normally distributed). Used for TMS practical in the course Experimental Methods 3.
"""

from psychopy.core import wait
import random
import serial

nr_trials = 25
isi_mu = 4
isi_std = 0.5

portname = 'COM6' # Change to COM PORT name on your device (check device manager)

isi_jittered = [random.gauss(isi_mu, isi_std) for _ in range(nr_trials)]
print(isi_jittered)

#ports = serial.tools.list_ports.comports()
port = serial.Serial(portname)

wait(5)

for i, isi in enumerate(isi_jittered):
    print('Trial ', str(i))
    port.write(1) # send trigger
    wait(isi)

port.close()
