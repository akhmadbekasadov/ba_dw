import time
import Adafruit_ADS1x15
#from threading import Timer


adc = Adafruit_ADS1x15.ADS1115()

count = 0
precount = 0
temp_voltage = 0.0
i = 1
GAIN = 1

time.sleep(15)


print('Reading ADS1115 values and writing to CSV')

while precount < 10:
        temp_voltage = adc.read_adc(0)

        precount = precount + 1
        time.sleep(0.07)


f = open('data.csv', 'w')

while count < 750:
	temp_voltage = adc.read_adc(0)
	#temp_voltage = temp_voltage
	print(temp_voltage)

        f.write(str(i) + "; " + str(temp_voltage) + "\n")

	time.sleep(0.03)

        i = i + 1
        count = count + 1
	#time.sleep(0.01)

	#Timer.Alarm(read_adc, 0.02, periodic=True)
	#threading.Timer(0.01, read_adc().start()
	#read_adc()

f.close()
print("\nFinished!\n")
