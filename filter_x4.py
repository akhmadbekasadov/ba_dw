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
x, timestamp, y0, y1, y2, y3 = np.loadtxt('live_data.csv', dtype=str, delimiter='; ', unpack=True)
y0 = y0.astype(np.float)
y1 = y1.astype(np.float)
y2 = y2.astype(np.float)
y3 = y3.astype(np.float)


n = int(x.size) # total number of samples
T = n / fs
t = np.linspace(0, T, n, endpoint=False)

#Create FFT
y0_offsetfree = y0 - np.mean(y0)
y1_offsetfree = y1 - np.mean(y1)
y2_offsetfree = y2 - np.mean(y2)
y3_offsetfree = y3 - np.mean(y3)

xf = scipy.fftpack.fftfreq(n, 1/fs)
xf = scipy.fftpack.fftshift(xf)

y0f = scipy.fftpack.fft(y0_offsetfree)
y1f = scipy.fftpack.fft(y1_offsetfree)
y2f = scipy.fftpack.fft(y2_offsetfree)
y3f = scipy.fftpack.fft(y3_offsetfree)

yf = y0f + y1f + y2f + y3f

yfreq = scipy.fftpack.fftshift(yf)

y_total = scipy.fftpack.ifft(yf)



# Filter the data
y_total_fil_lo = butter_lowpass_filter(y_total, cutoff, fs, order)
y_total_fil_hi = butter_bandpass_filter(y_total, lowcut, highcut, fs, order)



#Calc values for X-Axis (Plot)
x = np.linspace(0.0, n*T, n)
yf = scipy.fftpack.fft(y0)
xf = np.linspace(0.0, 1.0/(2.0*T), n/2)


#Find the Peaks (Heart, Breath)
heart_peaks_total, _ = find_peaks(-y_total_fil_hi, distance=16)
breath_peaks_total, _ = find_peaks(y_total_fil_lo, distance=65)


#Print Heart and Breath Frequency (all Time)
print "\nTotal Heartrate over all time: " + str(heart_peaks_total.size/T*60) + " Beats per Minute"
print "Total Breathrateover all time: " + str(breath_peaks_total.size/T*60) + " Breaths per Minute\n"


#Initialize values for printing Heart and Breath Frequency
heartrate = [0]*(len(heart_peaks_total)-1)
x_heartrate = [0]*(len(heart_peaks_total)-1)
breathrate = [0]*(len(breath_peaks_total)-1)
x_breathrate = [0]*(len(breath_peaks_total)-1)

mittlungswerte_heart = 30
mittlungswerte_breath = 6

temp_heartrate = []
temp_breathrate = []


#Calculate the Values for printing Heart Frequency
for i in range(0, len(heart_peaks_total)-1):
	temp_heartrate.append(60.0 / ((heart_peaks_total[i+1] - heart_peaks_total[i]) / fs))
	heartrate[i] = int(np.mean(temp_heartrate))
	x_heartrate[i] = heart_peaks_total[i+1]/fs
	if i >= mittlungswerte_heart:
		temp_heartrate.pop(0)

print("\nHeart frequency (2nd calculation):")
print("Median: " + str(np.median(heartrate)))
print("Mean: " + str(np.mean(heartrate)))
print("Datapoints: " + str(len(heartrate)))

#Calculate the Values for printing Breath Frequency
for i in range(0, len(breath_peaks_total)-1):
	temp_breathrate.append(60.0 / ((breath_peaks_total[i+1] - breath_peaks_total[i]) / fs))
	breathrate[i] = int(np.mean(temp_breathrate))
	x_breathrate[i] = breath_peaks_total[i+1]/fs
	if i >= mittlungswerte_breath:
		temp_breathrate.pop(0)

print("\nBreath frequency(2nd calculation):")
print("Median: " + str(np.median(breathrate)))
print("Mean: " + str(np.mean(breathrate)))
print("Length: " + str(len(breathrate)))



#Save times when a heartbeat has occurred in CSV
csv_heartrate = x_heartrate 
csv_heartrate = np.asarray(csv_heartrate)
csv_heartrate = csv_heartrate + float(timestamp[0])
np.savetxt('timestamp_of_heartbeats.csv', [csv_heartrate, heartrate], delimiter="; ", newline="\n", fmt='%f')
	

#Draw Plot
plt.subplot(9, 1, 1)
plt.plot(t, y0, 'b-', label='y0 Rawdata')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 2)
plt.plot(t, y1, 'b-', label='y1 Rawdata')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 3)
plt.plot(t, y2, 'b-', label='y2 Rawdata')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 4)
plt.plot(t, y3, 'b-', label='y3 Rawdata')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 5)
plt.plot(t, y_total, 'b-', label='y_total Rawdata')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 6)
plt.plot(heart_peaks_total/fs, y_total_fil_hi[heart_peaks_total], "x")
plt.plot(t, y_total_fil_hi, 'g-', linewidth=2, label='Heartbeat')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 7)
plt.plot(x_heartrate, heartrate, 'k-', linewidth=2, label='Heart rate')
plt.xlabel('Time [sec]')
plt.ylabel('Beats per Minute')
plt.grid()
plt.legend()

plt.subplot(9, 1, 8)
plt.plot(breath_peaks_total/fs, y_total_fil_lo[breath_peaks_total], "x")
plt.plot(t, y_total_fil_lo, 'r-', linewidth=2, label='Breathing')
plt.xlabel('Time [sec]')
plt.ylabel('Units')
plt.grid()
plt.legend()

plt.subplot(9, 1, 9)
plt.plot(x_breathrate, breathrate, 'k-', linewidth=2, label='Breath rate')
plt.xlabel('Time [sec]')
plt.ylabel('Breaths per Minute')
plt.grid()
plt.legend()


plt.subplots_adjust(hspace=0.35)
plt.show()
