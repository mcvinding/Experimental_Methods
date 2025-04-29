# Example code for sending EEG triggers using PsychoPy
# This code is for educational purposes and may need to be adapted for your specific setup.
# Overall idea: create a function called "trigger" that takes a code as an argument and sends it to the EEG system.

from psychopy import core, parallel, win

# OPTION #1: Using parallel port for sending triggers
# The function should also include a small delay to ensure the trigger is registered correctly.
from psychopy import parallel

# Define the port
port = parallel.ParallelPort(0x0378)  # 0x0378 is default address for parallel port on many machines. Change to match your machine.

def trigger(code):
    port.setData(code)
    core.wait(0.020)
    port.setData(0)

# OPTION #2: Using serial port for sending triggers
import serial

# Define the port
port = serial.Serial("COM4", 115200)  # address for serial port is COM4 in this example. Change to match your machine.

port.write(str.encode(code))


#####################################################################################
# OPTION #3: looking for the port type and setting it up accordingly

# Find relevant port type
try:
    port = serial.Serial("COM4", 115200)
    port_type = 'serial'
except NotImplementedError:
    port = parallel.setPortAddress(0x378)
    port_type = 'parallel'
except:
    port_type = 'Not set'
print('port type: {}'.format(port_type))

# Define the trigger function based on the port type
if port_type == 'parallel':                 # Parallel port
    def trigger(code=1):
        port.setData(code)
        print('trigger sent {}'.format(code))
elif port_type == 'serial':                 # Serial port
    def trigger(code=1):
        port.write(str.encode(code))
        print('trigger sent {}'.format(code))
else:                                       # No port set
    def trigger(code=1):
        print('trigger not sent {}'.format(code))



#####################################################################################
# Example usage of the trigger function:
# Whenever you want to send
win.callOnFlip(trigger, trig)   # "trig" = your trigger code


