# from https://github.com/ni/nidaqmx-python/blob/master/nidaqmx_examples/ai_voltage_sw_timed.py
# modified until it started working...
import pprint
import nidaqmx
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)

pp = pprint.PrettyPrinter(indent=4)

sample_rate = 1000
number_of_samples = 1000
samp_clk_terminal = ""

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
    task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)

    print('1 Channel 1 Sample Read: ')
    data = task.read()
    pp.pprint(data)

    data = task.read(number_of_samples_per_channel=1)
    pp.pprint(data)

    print('1 Channel N Samples Read: ')
    data = task.read(number_of_samples_per_channel=8)
    pp.pprint(data)

    #task.ai_channels.add_ai_voltage_chan("Dev3/ai1:3")

    #print('N Channel 1 Sample Read: ')
    #data = task.read()
    #pp.pprint(data)

    #print('N Channel N Samples Read: ')
    #data = task.read(number_of_samples_per_channel=2)
    #pp.pprint(data)
