import nidaq as daq
import time

myDAQ = daq.singlechannel('Dev2/ai0',48000,daq.constants['excitation']['voltage'],1024,daq.constants['coupling']['AC'])
data = myDAQ.read()

print('Took ' + str(len(data)) + ' datapoints')