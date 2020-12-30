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

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
    print('reading...')
    data = task.read(number_of_samples_per_channel=number_of_samples)
    sleep(duration)

print('plotting...')
import matplotlib.pyplot as plt
plt.plot(time[0:len(data)],data)
plt.xlabel('Time [s]')
plt.ylabel('Volts Output')
plt.show()