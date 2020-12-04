import nidaqmx # If it's already imported, we're good to go

class singlechannel:
	def __init__(self, physical_channel, sample_rate, ICP, number_of_samples, DCcoupling):
		self.name = str(physical_channel)
		# Validate if the name is a useful physical channel for us
		if ':' in self.name:
			raise NotImplementedError("We don't support multichannel in this library yet!")
		if not 'ai' in self.name.split('/')[-1]: # if the last slash item in the list isn't analog input
			raise NotImplementedError("Hm, that doesn't look like an analog input channel")
		
		# Cast a bunch of crap, for the sake of input validation
		self.SR = int(sample_rate)
		self.ICP = bool(ICP)
		self.N = int(number_of_samples)
		self.task = nidaqmx.Task()
		self.DCcoupling = bool(DCcoupling)
		
		# Let's not get crazy, now
		if ICP and DCcoupling:
			raise RuntimeError("You can't have DC coupling on with ICP.") # well, you can, but it's weird to
		
		# Create the task
		self.task.ai_channels.add_ai_voltage_chan(self.name)
		self.channelsettings(self.SR,self.ICP,self.N,self.DCcoupling)
	
	def channelsettings(self, sample_rate, ICP, number_of_samples, DCcoupling): # set or change task settings
		# Set clock timing
		self.task.timing.cfg_samp_clk_timing(sample_rate, source="", active_edge=nidaqmx.constants.Edge.RISING,samps_per_chan=number_of_samples)
		
		# Set ICP and coupling mode
		if ICP:
			self.task.ai_channels.all.ai_excit_val = 0.002 # got this from Chip's code somewhere -- hope it's right!
			self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC # must be AC coupled for ICP
		else:
			self.task.ai_channels.all.ai_excit_val = 0
			if self.DCcoupling:
				self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.DC
			else:
				self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC
	
	def read(self):
		return self.task.read(self.N)
	
	def readSingle(self):
		return self.task.read()