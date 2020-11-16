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

with nidaqmx.Task() as task:
	task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
	task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=number_of_samples)
	task.ai_channels[0].ai_excit_val = 0.002
	task.ai_channels[0].ai_coupling = nidaqmx.constants.Coupling.AC

	data = task.read(number_of_samples_per_channel=1024)

THDN(data,sample_rate)