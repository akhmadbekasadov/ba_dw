#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt, find_peaks
import scipy.fftpack
import matplotlib.pyplot as plt


#Filter functions
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
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
    y = lfilter(b, a, data)
    #y = filtfilt(b, a, data)
    return y


# Filter requirements.
order = 2
fs = 25.0        # sample rate, Hz
T = 30.0        # seconds
cutoff = 0.3 	 # desired cutoff frequency of the filter, Hz
lowcut = 3.0
highcut = 12.4


# Filter coefficients
b, a = butter_lowpass(cutoff, fs, order)
b, a = butter_bandpass(lowcut, highcut, fs, order)


n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)


#Load Rawdata from csv-File
x, y = np.loadtxt('data.csv', dtype=str, delimiter='; ', unpack=True)#, max_rows=300)
y = y.astype(np.float)


# Filter the data
y_fil_lo = butter_lowpass_filter(y, cutoff, fs, order)
y_fil_hi = butter_bandpass_filter(y, lowcut, highcut, fs, order)


#Calc values for X-Axis (Plot)
x = np.linspace(0.0, n*T, n)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), n/2)


#Find the Peaks (Heart, Breath)
heart_peaks, _ = find_peaks(-y_fil_hi, distance=15)
breath_peaks, _ = find_peaks(y_fil_lo, distance=60)


#Print Heart and Breath Frequency (all Time)
print "Heartrate: " + str(heart_peaks.size/T*60) + " Beats per Minute"
print "Breathrate: " + str(breath_peaks.size/T*60) + " Breaths per Minute"


#Initialize values for printing Heart and Breath Frequency
heartrate = [0]*(len(heart_peaks)-1)
x_heartrate = [0]*(len(heart_peaks)-1)

breathrate = [0]*(len(breath_peaks)-1)
x_breathrate = [0]*(len(breath_peaks)-1)

mittlungswerte_heart = 30
mittlungswerte_breath = 15

temp_heart = []
temp_breath = []

test = []

#Calculate the Values for printing Heart Frequency
for i in range(0, len(heart_peaks)-1):
	temp_heart.append(60.0 / ((heart_peaks[i+1] - heart_peaks[i]) / fs))
	heartrate[i] = int(np.mean(temp_heart))
	test.append(60.0 / ((heart_peaks[i+1] - heart_peaks[i]) / fs))
	x_heartrate[i] = heart_peaks[i+1]/fs
	if i >= mittlungswerte_heart:
		temp_heart.pop(0)
print("\nMedian: " + str(np.median(test)))
print("Länge: " + str(len(heartrate)))
print("Mittelwert: " + str(np.mean(heartrate)))


#Calculate the Values for printing Breath Frequency
for i in range(0, len(breath_peaks)-1):
	temp_breath.append(60.0 / ((breath_peaks[i+1] - breath_peaks[i]) / fs))
	breathrate[i] = int(np.mean(temp_breath))
	x_breathrate[i] = breath_peaks[i+1]/fs
	if i >= mittlungswerte_breath:
		temp_breath.pop(0)
print("\nMedian: " + str(np.median(breathrate)))
print("Länge: " + str(len(breathrate)))
print("Mittelwert: " + str(np.mean(breathrate)))


#Draw Plot
plt.subplot(5, 1, 1)
plt.plot(t, y, 'b-', label='Rawdata')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(5, 1, 2)
plt.plot(heart_peaks/fs, y_fil_hi[heart_peaks], "x")
plt.plot(t, y_fil_hi, 'g-', linewidth=2, label='Herzschlag')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(5, 1, 3)
plt.plot(x_heartrate, test, 'k-', linewidth=2, label='Herzfrequenz')
plt.xlabel('Time [sec]')
plt.ylabel('Beats per Minute')
plt.grid()
plt.legend()

plt.subplot(5, 1, 4)
plt.plot(breath_peaks/fs, y_fil_lo[breath_peaks], "x")
plt.plot(t, y_fil_lo, 'r-', linewidth=2, label='Atmung')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(5, 1, 5)
plt.plot(x_breathrate, breathrate, 'k-', linewidth=2, label='Atemfrequenz')
plt.xlabel('Time [sec]')
plt.ylabel('Breaths per Minute')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
