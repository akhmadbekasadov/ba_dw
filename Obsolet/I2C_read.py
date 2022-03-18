import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')

while True:
    print(str(adc.read_adc(0)))
    time.sleep(0.01)
