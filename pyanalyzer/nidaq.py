import nidaqmx # If it's already imported, we're good to go
import NIDAQconstants as constants # constants for coupling and excitation types

class singlechannel_read:
	def __init__(self, physical_channel, sample_rate, excitation, number_of_samples, coupling):
		# Validate (half-assedly) if the name contains a useful physical channel for us
		self.name = str(physical_channel)
		if ':' in self.name:
			raise NotImplementedError("We don't support multichannel in this library yet!")
		if not 'ai' in self.name.split('/')[-1]: # if the last slash item in the list isn't analog input
			raise NotImplementedError("Hm, that doesn't look like an analog input channel")
		
		# Create the task
		self.task = nidaqmx.Task()
		self.task.ai_channels.add_ai_voltage_chan(self.name)
		self.channelsettings(sample_rate,excitation,number_of_samples,coupling) # set up channel (also performs input validation)
	
	def __del__(self): # a destructor is required to properly close the task
		self.task.close()
	
	def channelsettings(self, sample_rate=None, excitation=None, number_of_samples=None, coupling=None): # set or change task settings
		# Check optional arguments (During first use in __init__(), all arguments must be set to `not None` or this will break. See line above)
		if sample_rate is None:
			sample_rate = self.SR
		if number_of_samples is None:
			number_of_samples = self.N
		if coupling is None:
			coupling = self.coupling
		if excitation is None:
			excitation = self.coupling
		
		# Cast a bunch of crap, for the sake of input validation
		self.SR = int(sample_rate)
		self.excitation = bool(excitation)
		self.N = int(number_of_samples)
		self.coupling = bool(coupling)
		
		# Let's not get crazy, now
		if self.excitation==constants.excitation.ICP and self.coupling==constants.coupling.DC:
			raise RuntimeError("You can't have DC coupling on with ICP.") # well, you can, but it's weird to
		if self.N <= 0:
			raise ValueError("You've got to read a positive number of points, silly goose")

		# Set clock timing
		self.task.timing.cfg_samp_clk_timing(self.SR, source="", active_edge=nidaqmx.constants.Edge.RISING,samps_per_chan=self.N)
		
		# Set ICP and coupling mode (a bit funky, should maybe separate into two separate sections, eventually)
		if self.excitation == constants.excitation.ICP: # if we're set to ICP
			self.task.ai_channels.all.ai_excit_val = 0.002 # got this from Chip's code somewhere -- hope it's right!
			self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC # must be AC coupled for ICP
		else:
			self.task.ai_channels.all.ai_excit_val = 0
			if self.coupling == constants.coupling.DC:
				self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.DC
			else:
				self.task.ai_channels.all.ai_coupling = nidaqmx.constants.Coupling.AC
	
	def read(self,N=None): # you can optionally pass an N, as long as it's less than self.N
		if N is None:
			N = self.N
		else:
			if N > self.N:
				raise ValueError("You cannot set an N value larger than number_of_samples set for the channel")
			#if N == 1
			#	raise ValueError("Use readSingle() to read a single point") # I suppose this isn't completely necessary...
		return self.task.read(N)
	
	def readSingle(self):
		return self.task.read()

""" class multichannel:
	def __init__(self, physical_channel, sample_rate, excitation, number_of_samples, coupling):
		# Validate (half-assedly) if the name contains a useful physical channel for us
		self.name = str(physical_channel)
		if ':' in self.name:
			raise NotImplementedError("We don't support multichannel in this library yet!")
		if not 'ai' in self.name.split('/')[-1]: # if the last slash item in the list isn't analog input
			raise NotImplementedError("Hm, that doesn't look like an analog input channel")
		
		# Create the task
		self.task = nidaqmx.Task()
		self.task.ai_channels.add_ai_voltage_chan(self.name)
		self.Nchannels = len(self.task.ai_channels) # this variable used in various locations (will not change after initial setup)
		self.channelsettings(self.SR,self.ICP,self.N,self.DCcoupling) # set up channel (also performs input validation)
	
	def channelsettings(self, sample_rate=None, excitation=None, number_of_samples=None, DCcoupling=None): # set or change task settings
		# Check optional arguments (During first use in __init__(), all arguments must be set to `not None` or this will break. See line above)
		if sample_rate is None:
			sample_rate = self.SR
		
		if number_of_samples is None:
			number_of_samples = self.N
		
		if type(coupling) is list or type(coupling) is tuple:
			for i in range(len(coupling)):
				if coupling(i) is None:
					coupling(i) = self.DCcoupling(i)
		elif coupling is None:
			coupling = self.DCcoupling
		else:
			raise ValueError("coupling must be a tuple or list for multichannel")
		
		if type(excitation) is list or type(excitation) is tuple:
			for i in range(len(excitation)):
				if excitation(i) is None:
					excitation(i) = self.ICP(i)
		elif excitation is None:
			excitation = self.ICP
		else:
			raise ValueError("excitation must be a tuple or list for multichannel")
		
		# Cast a bunch of crap, for the sake of input validation
		self.SR = int(sample_rate)
		self.N = int(number_of_samples)
		for i in range(len(coupling)):
			self.DCcoupling(i) = bool(coupling(i))
		for i in range(len(excitation)):
			self.ICP(i) = bool(excitation(i))
		
		# Let's not get crazy, now
		if self.ICP and self.DCcoupling:
			raise RuntimeError("You can't have DC coupling on with ICP.") # well, you can, but it's weird to
		if self.N <= 0:
			raise ValueError("You've got to read a positive number of points, silly goose")
		if len(ICP) != len(DCcoupling):
			raise ValueError("ICP and DCcoupling should be boolean arrays of the same length!")
		if len(ICP) != self.Nchannels:
			raise ValueError("ICP and DCcoupling should have the same number of elements as the number of channels you're using")
		
		# Set clock timing
		self.task.timing.cfg_samp_clk_timing(self.SR, source="", active_edge=nidaqmx.constants.Edge.RISING,samps_per_chan=self.N)
		
		# Set ICP and coupling mode
		for i in range(self.Nchannels):
			if self.ICP[i]:
				self.task.ai_channels.[i].ai_excit_val = 0.002 # got this value from Chip's code somewhere -- hope it's right!
				self.task.ai_channels.[i].ai_coupling = nidaqmx.constants.Coupling.AC # must be AC coupled for ICP
			else:
				self.task.ai_channels.[i].ai_excit_val = 0
				if self.DCcoupling:
					self.task.ai_channels.[i].ai_coupling = nidaqmx.constants.Coupling.DC
				else:
					self.task.ai_channels.[i].ai_coupling = nidaqmx.constants.Coupling.AC
	
	def read(self,N=None): # you can optionally pass an N, as long as it's less than self.N
		if N is None:
			N = self.N
		else:
			if N > self.N:
				raise ValueError("You cannot set an N value larger than number_of_samples set for the channel")
			#if N == 1
			#	raise ValueError("Use readSingle() to read a single point") # I suppose this isn't completely necessary...
		return self.task.read(N)
	
	def readSingle(self):
		return self.task.read() """
