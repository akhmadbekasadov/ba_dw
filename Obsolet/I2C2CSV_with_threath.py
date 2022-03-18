import time
import Adafruit_ADS1x15
import datetime, threading, time
#from threading import Timer


adc = Adafruit_ADS1x15.ADS1115()

count = 0
precount = 0
temp_voltage0 = 0.0
temp_voltage1 = 0.0
temp_voltage2 = 0.0
i = 1
GAIN = 1

time.sleep(15)


next_call = time.time()


def read():
	global next_call, i, count, temp_voltage0, temp_voltage1, temp_voltage1

	if(count < 749):
		next_call = next_call + 0.04
        	threading.Timer( next_call - time.time(), read).start()

	f = open('data.csv', 'a')

	temp_voltage0 = adc.read_adc(0)
	temp_voltage1 = adc.read_adc(1)
	temp_voltage2 = adc.read_adc(2)
	time.sleep(0.005)

        f.write(str(i) + "; " + str(temp_voltage0) + "; " + str(temp_voltage1) + "; " + str(temp_voltage2) + "\n")
	print (str(temp_voltage0))

	i = i + 1
        count = count + 1

	f.close()

next_call = next_call + 1.00
threading.Timer( next_call - time.time(), read).start()


print("\nStarting\n")
