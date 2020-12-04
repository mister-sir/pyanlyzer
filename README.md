# Pyanalzer

Pyanalyzer is a python package for doing various data acquision tasks and signal processing using NI DAQmx.

## Installation

This package is currently a bit hard to install -- more to come on that later.

## Usage

Here's a simple example. More to come.

```python
import modalshop.nidaq as daq

myTask = daq.singlechannel(physical_channel="Dev3/ai0", sample_rate=50000, ICP=True, number_of_samples=1000, DCcoupling=False)

data = myTask.read() # returns a numpy array of volts, I think
```

## Contributing
Pull requests are welcome. You can also open issues in the bug tracker if you spot an issue.

## License
[MIT](https://choosealicense.com/licenses/mit/)