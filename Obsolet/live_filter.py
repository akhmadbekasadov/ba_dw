#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

# Imports
import numpy as np
import scipy.fftpack
from drawnow import *
import Adafruit_ADS1x15
import datetime, threading, time
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, filtfilt, find_peaks

# Create objets
adc = Adafruit_ADS1x15.ADS1115()

# Create variables
y0 = []
y1 = []
y2 = []
y3 = []

fill = 1
counter = -100
y_fil_lo = []
y_fil_hi = []
temp_breath = []
next_call = time.time()
next_call_calc = time.time()

#Filter functions
def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# Timer - to the time exact reading of the data
def read():
        global next_call, fill, counter, fs, T, y0, y1, y2, y3

	# Set timer of next interrupt:
	next_call = next_call + 0.04
        threading.Timer( next_call - time.time(), read).start()
	#print(time.time())
	# Save the queried value:
	f=open('live_data.csv','a')

	temp_read0 = adc.read_adc(0)
        temp_read1 = adc.read_adc(1)
        temp_read2 = adc.read_adc(2)
	temp_read3 = adc.read_adc(3)

	y0.append(temp_read0)
	y1.append(temp_read1)
	y2.append(temp_read2)
	y3.append(temp_read3)


        f.write(str(fill) + "; " + str(temp_read0) + "; " + str(temp_read1) + "; " + str(temp_read2) + "; " + str(temp_read3) + "\n")

	f.close


	# Delete old values if they exist:
        if (fill >= ((T*fs)+1)):
                y0.pop(0)
                y1.pop(0)
                y2.pop(0)
                y3.pop(0)

        fill = fill + 1



# Calculate the Heart and Breath Frequency:
def calc():
	global next_call_calc, temp_breath, y_fil_lo, y_fil_hi, y0, y1, y2, y3

        # Set timer of next interrupt:
        next_call_calc = next_call_calc + (T) # + (T/2)
        threading.Timer( next_call_calc - time.time(), calc).start()

        print("\n--------------------------CALC NOW")

	#remove offset
        y0_offsetfree = y0 - np.mean(y0)
        y1_offsetfree = y1 - np.mean(y1)
        y2_offsetfree = y2 - np.mean(y2)
        y3_offsetfree = y3 - np.mean(y3)

	#FFT
        y0f = scipy.fftpack.fft(y0_offsetfree)
        y1f = scipy.fftpack.fft(y1_offsetfree)
        y2f = scipy.fftpack.fft(y2_offsetfree)
        y3f = scipy.fftpack.fft(y3_offsetfree)

	#Sum
        yf = y0f + y1f + y2f + y3f

	#IFFT
        y_total = scipy.fftpack.ifft(yf)

	#Filter
        y_fil_lo = butter_lowpass_filter(y_total, cutoff, fs, order_lo)
	y_fil_hi = butter_bandpass_filter(y_total, lowcut, highcut, fs, order_hi)


	# Find the Peaks (Heart, Breath):
	heart_peaks, _ = find_peaks(-y_fil_hi, distance=13)
 	breath_peaks, _ = find_peaks( y_fil_lo, distance=75)
	#Calculate the Values for printing Heart Frequency
	temp_heart = []
	for i in range(0, len(heart_peaks)-1):
        	temp_heart.append(60.0 / ((heart_peaks[i+1] - heart_peaks[i]) / fs))
        try:
		heartrate_mean = int(np.mean(temp_heart))
		heartrate_median = int(np.median(temp_heart))
		# Prints
		print("\nHearbeat:")
		print("Median: " + str(heartrate_median))
		print("Mittelwert: " + str(heartrate_mean))
		print("Laenge: " + str(len(temp_heart)))
	except:
		pass

	#Calculate the Values for printing Breath Frequency
	for i in range(0, len(breath_peaks)-1):
        	temp_breath.append(60.0 / ((breath_peaks[i+1] - breath_peaks[i]) / fs))
		if len(temp_breath) >= 5:
			temp_breath.pop(0)
        try:
		breathrate_mean = int(np.mean(temp_breath))
		breathrate_median = int(np.median(temp_breath))
		# Prints:
		print("\nRespiration:")
		print("Median: " + str(breathrate_median))
		print("Mittelwert: " + str(breathrate_mean))
		print("Laenge: " + str(len(temp_breath)))
	except:
		pass


# Filter requirements.
order_hi = 2
order_lo = 5
fs = 25.0        # sample rate, Hz
T = 16.0         # duration, seconds z.B.: 2, 4, 8, 16, 32
cutoff = 0.3 	 # desired cutoff frequency of the filter, Hz
lowcut = 3.0     # desired lower cut-off frequency of the filter, Hz
highcut = 10.0   # desired upper cut-off frequency of the filter, Hz
n = int(T * fs)  # total number of samples


# Filter coefficients
#b, a = butter_lowpass(cutoff, fs, order)
#b, a = butter_bandpass(lowcut, highcut, fs, order)

print("Starting up...")

next_call = next_call + 2
threading.Timer( next_call - time.time(), read).start()
print("Part 1/3")

next_call_calc = next_call_calc + 24
threading.Timer( next_call_calc - time.time(), calc).start()
print("Part 2/3")
