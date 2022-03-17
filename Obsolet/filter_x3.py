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
cutoff = 0.3 	 # desired cutoff frequency of the filter, Hz
lowcut = 3.0
highcut = 12.4


# Filter coefficients
b, a = butter_lowpass(cutoff, fs, order)
b, a = butter_bandpass(lowcut, highcut, fs, order)



#Load Rawdata from csv-File
x, y0, y1, y2 = np.loadtxt('live_data.csv', dtype=str, delimiter='; ', unpack=True)
y0 = y0.astype(np.float)
y1 = y1.astype(np.float)
y2 = y2.astype(np.float)

n = int(x.size) # total number of samples
T = n / fs
t = np.linspace(0, T, n, endpoint=False)

#Create FFT
y0_offsetfree = y0 - np.mean(y0)
y1_offsetfree = y1 - np.mean(y1)
y2_offsetfree = y2 - np.mean(y2)

xf = scipy.fftpack.fftfreq(n, 1/fs)
xf = scipy.fftpack.fftshift(xf)

y0f = scipy.fftpack.fft(y0_offsetfree)
y1f = scipy.fftpack.fft(y1_offsetfree)
y2f = scipy.fftpack.fft(y2_offsetfree)

yf = y0f + y1f + y2f

yfreq = scipy.fftpack.fftshift(yf)

y_total = scipy.fftpack.ifft(yf)



# Filter the data
y0_fil_lo = butter_lowpass_filter(y0_offsetfree, cutoff, fs, order)
y0_fil_hi = butter_bandpass_filter(y0_offsetfree, lowcut, highcut, fs, order)

y1_fil_lo = butter_lowpass_filter(y1_offsetfree, cutoff, fs, order)
y1_fil_hi = butter_bandpass_filter(y1_offsetfree, lowcut, highcut, fs, order)

y2_fil_lo = butter_lowpass_filter(y2_offsetfree, cutoff, fs, order)
y2_fil_hi = butter_bandpass_filter(y2_offsetfree, lowcut, highcut, fs, order)

y_total_fil_lo = butter_lowpass_filter(y_total, cutoff, fs, order)
y_total_fil_hi = butter_bandpass_filter(y_total, lowcut, highcut, fs, order)



#Calc values for X-Axis (Plot)
x = np.linspace(0.0, n*T, n)
yf = scipy.fftpack.fft(y0)
xf = np.linspace(0.0, 1.0/(2.0*T), n/2)


#Find the Peaks (Heart, Breath)
heart_peaks0, _ = find_peaks(-y0_fil_hi, distance=13)
breath_peaks0, _ = find_peaks(y0_fil_lo, distance=75)

heart_peaks1, _ = find_peaks(-y1_fil_hi, distance=13)
breath_peaks1, _ = find_peaks(y1_fil_lo, distance=75)

heart_peaks2, _ = find_peaks(-y2_fil_hi, distance=13)
breath_peaks2, _ = find_peaks(y2_fil_lo, distance=75)

heart_peaks_total, _ = find_peaks(-y_total_fil_hi, distance=13)
breath_peaks_total, _ = find_peaks(y_total_fil_lo, distance=75)


#Print Heart and Breath Frequency (all Time)
print "Heartrate: " + str(heart_peaks_total.size/T*60) + " Beats per Minute"
print "Breathrate: " + str(breath_peaks_total.size/T*60) + " Breaths per Minute"


#Initialize values for printing Heart and Breath Frequency
#heartrate0 = [0]*(len(heart_peaks0)-1)
#x_heartrate = [0]*(len(heart_peaks0)-1)

#breathrate0 = [0]*(len(breath_peaks0)-1)
#x_breathrate = [0]*(len(breath_peaks0)-1)

#mittlungswerte_heart = 30
#mittlungswerte_breath = 15

#temp_heart = []
#temp_breath = []

#test = []

#Calculate the Values for printing Heart Frequency
#for i in range(0, len(heart_peaks)-1):
#	temp_heart.append(60.0 / ((heart_peaks[i+1] - heart_peaks[i]) / fs))
#	heartrate[i] = int(np.mean(temp_heart))
#	test.append(60.0 / ((heart_peaks[i+1] - heart_peaks[i]) / fs))
#	x_heartrate[i] = heart_peaks[i+1]/fs
#	if i >= mittlungswerte_heart:
#		temp_heart.pop(0)
#print("\nMedian: " + str(np.median(test)))
#print("Länge: " + str(len(heartrate)))
#print("Mittelwert: " + str(np.mean(heartrate)))


#Calculate the Values for printing Breath Frequency
#for i in range(0, len(breath_peaks)-1):
#	temp_breath.append(60.0 / ((breath_peaks[i+1] - breath_peaks[i]) / fs))
#	breathrate[i] = int(np.mean(temp_breath))
#	x_breathrate[i] = breath_peaks[i+1]/fs
#	if i >= mittlungswerte_breath:
#		temp_breath.pop(0)
#print("\nMedian: " + str(np.median(breathrate)))
#print("Länge: " + str(len(breathrate)))
#print("Mittelwert: " + str(np.mean(breathrata)))

#Draw Plot
plt.subplot(9, 1, 1)
plt.plot(t, y0, 'b-', label='Rawdata')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 2)
plt.plot(heart_peaks0/fs, y0_fil_hi[heart_peaks0], "x")
plt.plot(t, y0_fil_hi, 'g-', linewidth=2, label='Herzschlag')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 3)
plt.plot(t, y1, 'b-', label='Rawdata')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 4)
plt.plot(heart_peaks1/fs, y1_fil_hi[heart_peaks1], "x")
plt.plot(t, y1_fil_hi, 'g-', linewidth=2, label='Herzschlag')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 5)
plt.plot(t, y2, 'b-', label='Rawdata')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 6)
plt.plot(heart_peaks2/fs, y2_fil_hi[heart_peaks2], "x")
plt.plot(t, y2_fil_hi, 'g-', linewidth=2, label='Herzschlag')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 7)
plt.plot(t, y_total, 'b-', label='iFFT -> Rawdata')
plt.grid()
plt.legend()

plt.subplot(9, 1, 8)
plt.plot(heart_peaks_total/fs, y_total_fil_hi[heart_peaks_total], "x")
plt.plot(t, y_total_fil_hi, 'g-', linewidth=2, label='Herzschlag')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(9, 1, 9)
plt.plot(breath_peaks_total/fs, y_total_fil_lo[breath_peaks_total], "x")
plt.plot(t, y_total_fil_lo, 'r-', linewidth=2, label='Atmung')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()


plt.subplots_adjust(hspace=0.35)
plt.show()
