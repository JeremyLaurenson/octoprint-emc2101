import sys
import time
import board
from adafruit_tca9548a import TCA9548A
from adafruit_emc2101 import EMC2101


i2c = board.I2C()  # uses board.SCL and board.SDA
FAN_MAX_RPM = 1700



def main():
	# total arguments
	n = len(sys.argv)
	if n != 3:
		print("say_whut")
		sys.exit(2) 

	dutyCycle=int(sys.argv[2])
	channel = int(sys.argv[1])
	if(channel==0):
		emc = EMC2101(i2c)
	else:
		emc = EMC2101(tca[channel-1])
	emc.manual_fan_speed = dutyCycle
	temperature = emc.internal_temperature
	fanspeed = emc.fan_speed
	print('{0:0.1f} | {1:0.1f}'.format(temperature, fanspeed))

if __name__ == "__main__":
	main()



