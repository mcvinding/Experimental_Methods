# A simple oddball experiment for EEG demo
#   cf Näätänen et al 1978 (https://doi.org/10.1016/0001-6918(78)90006-9)
from psychopy import visual, core, sound, event, parallel
import random
import serial
import pylsl

# Parameters
n_trials        = 1000  # Total number of trials
use_lsl         = False

# Create a window
win = visual.Window(fullscr=False, color='black', screen=1)

################################################################################
# FUNCITONS
################################################################################
# EEG TRIGGER (simple)
#def trigger(code)
#    parallel.setData(code)
#    core.wait(0.020)
#    parallel.setData(0)

# EEG TRIGGER (read port)
if use_lsl is True:
    port_type = 'lsl'
    
    name = "triggerTiming"
    strm_type = "Markers"
    chans = 1
    srate = 1000.0
    fmt = 'string'

    info = pylsl.StreamInfo(
        name=name,
        type=strm_type,
        channel_count=chans,
        nominal_srate=srate,
        channel_format=fmt,
    #    source_id=None,
    )
    outlet = pylsl.StreamOutlet(info)
    print("Now publishing stream:", info.name(), info.type(), info.channel_count(), "channels at", info.nominal_srate(), "Hz")
else:
    try:
        port = serial.Serial("COM9", 115200)  # Make sure COM port matches your system
        port_type = 'serial'
    except NotImplementedError:
        port = parallel.setPortAddress(0x378) # 0x378 is the address for parallel port on many machines
        port_type = 'parallel'
    except:
        port_type = 'Not set'

    print('port type: {}'.format(port_type))

# Make trigger functions
if port_type == 'lsl':
    def trigger(code=1):
        outlet.push_sample(str(code))
        print("Pushing marker {}" .format(code))
elif port_type == 'parallel':
    def trigger(code=1):
        port.setData(code)
        print('trigger sent {}'.format(code))
elif port_type == 'serial':
    def trigger(code=1):
        port.write(code.to_bytes(1, 'big'))
        print('trigger sent {}'.format(code))
else:
    def trigger(code=1):
        print('trigger not sent {}'.format(code))

################################################################################
# RUN
################################################################################

# Define the standard and deviant sounds
standard_tone = sound.Sound(1000, sampleRate=44100, secs=0.031, stereo=True)             # Standard tone
figure = visual.rect.Rect(win, fillColor='white', pos=(1,-1))
blank_text = visual.TextStim(win, text='', color='red')

    # Trial loop
for tt in range(n_trials):
    nextFlip = win.getFutureFlipTime()
        
    if tt % 2 == 0:
        figure.draw()
        trig = 1
    else:
        standard_tone.play(when = nextFlip)
        trig = 2
          
    win.callOnFlip(trigger, trig)        
    win.flip()                                  # Update the window to show the visual stimulus
    core.wait(0.10)
    blank_text.draw()
    win.flip()
    core.wait(0.20)     # Wait extra 250 ms between tones
        
    # Check for quit (the Esc or q key)
    if event.getKeys(keyList=["escape","q"]):
        break

    # Close the window
win.close()
core.quit()





