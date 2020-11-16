# Added ICP, and also demonstrated multichannel
import pprint
import nidaqmx
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)

pp = pprint.PrettyPrinter(indent=4)

sample_rate = 1000
number_of_samples = 1000
samp_clk_terminal = ""

task = nidaqmx.Task()
task2 = nidaqmx.Task()

#task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
#task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
##task.ai_channels.all.ai_excit_val = 0.002
##task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC
#task.ai_channels[0].ai_excit_val = 0.002
#task.ai_channels[0].ai_coupling = nidaqmx.constants.Coupling.AC

#print('1 Channel 1 Sample Read: ')
#data = task.read()
#pp.pprint(data)

#data = task.read(number_of_samples_per_channel=1)
#pp.pprint(data)

#print('1 Channel N Samples Read: ')
#data = task.read(number_of_samples_per_channel=8)
#pp.pprint(data)

task2.ai_channels.add_ai_voltage_chan("Dev3/ai2:3")
task2.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
task2.ai_channels.all.ai_excit_val = 0.002
task2.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC

print('N Channel 1 Sample Read: ')
data = task2.read()
pp.pprint(data)

print('N Channel N Samples Read: ')
data = task2.read(number_of_samples_per_channel=8)
pp.pprint(data)
