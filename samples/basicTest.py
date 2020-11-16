from PyDAQmx import *
import numpy

myTask = Task()
read = int32()
data = numpy.zeros((1000,), dtype=numpy.float64)

# DAQmx Configure Code
myTask.CreateAIVoltageChan(b"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None) # Use Dev1/ai0, default config, -10 to 10 Volts, units of volts, no custom scaling
myTask.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000) # use the onboard clock, SR of 10000 Hz, rising edge (whatever, I don't care), Finite number of samples, acquire 1000 samples

# DAQmx Start Code
myTask.StartTask()

# DAQmx Read Code
myTask.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

print("Acquired %d points",read.value)
