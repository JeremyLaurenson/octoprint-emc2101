from sre_constants import NOT_LITERAL
import time
import board
import sys
from adafruit_tca9548a import TCA9548A
from adafruit_emc2101 import EMC2101




FAN_MAX_RPM = 1700


i2c = board.I2C()  # uses board.SCL and board.SDA
directmode = False

try:
	# Create the TCA9548A object and give it the I2C bus
	tca = TCA9548A(i2c)
	scan = tca.scan()
except:
	directmode=True

if directmode:
	emc = EMC2101(i2c)
else:
	emc = EMC2101(tca[0])



def getTemp():
	return(emc.internal_temperature)

def getSpeed():
    return(emc.fan_speed)

def main():

	if len(sys.argv) == 2:
		channel = int(sys.argv[1])
	else:
		print('-1 | -1')
		sys.exit(1)
	if(channel==0):
		emc = EMC2101(i2c)
	else:
		emc = EMC2101(tca[channel-1])
		
	try:
		temperature = getTemp()
		fanspeed = getSpeed()
		print('{0:0.1f} | {1:0.1f}'.format(temperature, fanspeed))
	except:
		print('-1 | -1')

if __name__ == "__main__":
	main()

