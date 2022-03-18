from drawnow import *
import numpy as np
import Adafruit_ADS1x15
import matplotlib.pyplot as plt
import time

adc = Adafruit_ADS1x15.ADS1115()

value = []
plt.ion()  # Tell matplotlib you want interactive mode to plot live data
count = 0


def makeFig():
	plt.title('Live Data')
	plt.grid(True)
	plt.ylabel('Value')
	plt.xlabel('Samples')
	plt.plot(value, 'ro-')

#while(True):
#	value.append(adc.read_adc(0))
#        drawnow(makeFig)
#        plt.pause(.000001)
#        count += 1
#        if count > 40:
#            value.pop(0)


fig = plt.figure()

while(True):
	plt.plot(adc.read_adc(0), c='black')
	fig.canvas.draw()

	image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
	image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
