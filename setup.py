import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pyanalyzer",
	version="0.0.1",
	author="Brian Ulrich",
	author_email="bulrich@modalshop.com",
	description="A set of tools for data acquisition and processing using NI DAQ hardware",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/mister-sir/pyanlyzer",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 2 - Pre-Alpha"
	],
	install_requires=[ # so far only nidaqmx, but numpy and scipy are very helpful to have
		#'numpy',
		#'scipy',
		'nidaqmx'
	],
	python_requires='>=3.6',
)