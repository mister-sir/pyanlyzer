def THD_N(signal, SR):
	raise NotImplementedError("This function isn't complete yet!")
	# THD_N() is heavily based on code licensed as follows:
	# The MIT License (MIT)
	
	# Copyright (c) 2016 endolith@gmail.com
	
	# Permission is hereby granted, free of charge, to any person obtaining a copy
	# of this software and associated documentation files (the "Software"), to deal
	# in the Software without restriction, including without limitation the rights
	# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	# copies of the Software, and to permit persons to whom the Software is
	# furnished to do so, subject to the following conditions:
	
	# The above copyright notice and this permission notice shall be included in all
	# copies or substantial portions of the Software.
	
	# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	# SOFTWARE.
	"""Measure the THD+N for a signal and print the results
	
	Prints the estimated fundamental frequency and the measured THD+N.  This is
	calculated from the ratio of the entire signal before and after
	notch-filtering.
	
	This notch-filters by nulling out the frequency coefficients ±10% of the
	fundamental
	"""
	
	from scipy.signal import kaiser # for kaiser windowing ## TODO: allow other windows??
	from numpy.fft import rfft, irfft # for FFT
	from numpy import argmax, mean, log10, log, ceil, concatenate, zeros # various math things we need
	
	# Get rid of DC and window the signal
	signal -= mean(signal) # TODO: Do this in the frequency domain, and take any skirts with it?
	windowed = signal * kaiser(len(signal), 100)
	del signal
	
	# Zero pad to nearest power of two
	new_len = int(2**ceil( log(len(windowed)) / log(2) ))
	windowed = concatenate((windowed, zeros(new_len - len(windowed))))
	
	# Measure the total signal before filtering but after windowing
	total_rms = rms_flat(windowed)
	
	# Find the peak of the frequency spectrum (fundamental frequency)
	f = rfft(windowed)
	i = argmax(abs(f))
	true_i = parabolic(log(abs(f)), i)[0]
	print('Frequency: %f Hz' % (sample_rate * (true_i / len(windowed))))
	
	# Filter out fundamental by throwing away values ±10%
	lowermin = int(true_i - 0.1 * true_i)
	uppermin = int(true_i + 0.1 * true_i)
	f[lowermin: uppermin] = 0
	
	# Transform noise back into the time domain and measure it
	noise = irfft(f)
	THDN = rms_flat(noise) / total_rms
	
	# TODO: RMS and A-weighting in frequency domain?
	
	# Apply A-weighting to residual noise (Not normally used for distortion,
	# but used to measure dynamic range with -60 dBFS signal, for instance)
	#weighted = A_weight(noise, sample_rate)
	#THDNA = rms_flat(weighted) / total_rms
	
	#print("THD+N:     %.4f%% or %.1f dB"    % (THDN  * 100, 20 * log10(THDN)))
	#print("A-weighted: %.4f%% or %.1f dB(A)" % (THDNA * 100, 20 * log10(THDNA)))
	return THDN # returns THD+N as a decimal