import numpy as np
from time import sleep
import nidaqmx
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)

# Input stuff
sample_rate = 48000 # Hz
freq = 100 # Hz
duration = 2 # seconds

# Parameters
number_of_samples = 2*sample_rate
samp_clk_terminal = ""

# Generate signal
time = np.arange(0, duration*10, 1/sample_rate) # make 10 times as much data as we're trying to measure...
signal = np.sin(time*2*3.14159265*freq)*6

with nidaqmx.Task() as writetask:
    writetask.ao_channels.add_ao_voltage_chan("Dev2/ao0")
    writetask.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
    print('writing')
    writetask.write(signal, auto_start=True)

with nidaqmx.Task() as readtask:
    readtask.ai_channels.add_ai_voltage_chan("Dev2/ai1")
    readtask.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
    print('reading...')
    data = readtask.read(number_of_samples_per_channel=number_of_samples)
    sleep(duration)

print('plotting...')
import matplotlib.pyplot as plt
plt.plot(time[0:len(data)],data)
plt.xlabel('Time [s]')
plt.ylabel('Volts Output')
plt.show()