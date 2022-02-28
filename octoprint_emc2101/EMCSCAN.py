from sre_constants import NOT_LITERAL
import time
import board
from adafruit_tca9548a import TCA9548A
from adafruit_emc2101 import EMC2101




i2c = board.I2C()  # uses board.SCL and board.SDA

# First, we scan the native i2c bus for an EMC2101
addresses = i2c.scan()
isFound=False
for address in addresses:
	if(address==0x4c):
		print("0 | 2101")
		isFound=True
if not isFound:
	print("0 | Not found")

tca = TCA9548A(i2c)
try:
	for channel in range(8):
		if tca[channel].try_lock():
			isFound=False
			addresses = tca[channel].scan()
			for address in addresses:
				if(address==0x4c):
					print("{} | 2101".format(channel+1))
					isFound=True
			if not isFound:
				print("{} | Not found".format(channel+1))
except:
	for channel in range(8):
		print("{} | Not Found".format(channel+1))