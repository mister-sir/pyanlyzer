def includeRelative(subfolder):
	import os, sys, inspect
	# Use this if you want to include modules from a subfolder
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],subfolder)))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)

includeRelative('libraries')
from waveform_analyzer.thd_analyzer import THDN

import nidaqmx
from nidaqmx.constants import (Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)
import matplotlib.pyplot as plt
from numpy import linspace
from time import sleep

sample_rate = 50000
seconds = 2
Nsamples = sample_rate*seconds
samp_clk_terminal = ""

with nidaqmx.Task() as task:
	task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
	task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=Nsamples)
	# These lines perform ICP signal conditioning
#	task.ai_channels[0].ai_excit_val = 0.002
#	task.ai_channels[0].ai_coupling = nidaqmx.constants.Coupling.AC
	print("Reading data... " + str(seconds) + " seconds at sample rate " + str(sample_rate) + " Hz")
	sleep(seconds)
	data = task.read(number_of_samples_per_channel=Nsamples)

THDN(data,sample_rate)

endTime = seconds-(1/sample_rate);
t = linspace(0,endTime,Nsamples)

plt.plot(data)
plt.show()
