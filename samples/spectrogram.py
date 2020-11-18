import nidaqmx
from nidaqmx.constants import (Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)
import matplotlib.pyplot as plt
from numpy import linspace
from time import sleep
from scipy import signal
#from scipy.fft import fftshift

sample_rate = 50000
seconds = 2
Nsamples = sample_rate*seconds
samp_clk_terminal = ""

with nidaqmx.Task() as task:
	task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
	task.timing.cfg_samp_clk_timing(sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,samps_per_chan=Nsamples)
	task.ai_channels[0].ai_excit_val = 0.002
	task.ai_channels[0].ai_coupling = nidaqmx.constants.Coupling.AC
	print("Reading data... " + str(seconds) + " seconds at sample rate " + str(sample_rate) + " Hz")
	sleep(seconds)
	data = task.read(number_of_samples_per_channel=Nsamples)

f, t, Sxx = signal.spectrogram(data, sample_rate)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
