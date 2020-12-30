import nidaq as daq
import time

print('imports done')
with daq.singlechannel('Dev2/ai0',48000,daq.constants['excitation']['voltage'],1024,daq.constants['coupling']['AC']) as myDAQ:
    data = myDAQ.read()
print('reading done')
print(data)
print('sleeping')
time.sleep(10)
print('bye!')