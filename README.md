# pyanalyzer

This package handles data acquisition using NI DAQ hardware such as the PCI-4461 or the USB-4431, among other devices. It also has some rudimentary signal analysis functions in the works.

## Installation

Download the repository and open a command prompt inside it. Run `py -m pip install .`. Currently the module is a little wonky and doens't like to install right. Work in progress, pre-pre-alpha.

## Usage

Here's a simple example. More to come.

```python
import pyanalyzer.nidaq as daq

myTask = daq.singlechannel(physical_channel="Dev3/ai0", sample_rate=50000, excitation=daq.constants.excitation.ICP , number_of_samples=1000, coupling=daq.constants.coupling.AC)

data = myTask.read() # returns an array of voltage values
```

## Contributing
Pull requests are welcome. You can also open issues in the bug tracker if you spot an issue.

## License
[MIT](https://choosealicense.com/licenses/mit/)