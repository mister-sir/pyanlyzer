import nidaq as daq # data acquisition
import NIDAQconstants as constants # constants for coupling and excitation types

myDAQ = daq.singlechannel('Dev2/ai0',48000,constants.excitation.voltage,1024,constants.coupling.AC)
data = myDAQ.read()

print('Took ' + str(len(data)) + ' datapoints')