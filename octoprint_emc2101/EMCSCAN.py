from sre_constants import NOT_LITERAL
import time
import board
import adafruit_tca9548a
from adafruit_emc2101 import EMC2101


i2c = board.I2C()  # uses board.SCL and board.SDA
addresses = i2c.scan()
isFound=False
for address in addresses:
	if(address==0x4c):
		print("0 | 2101")
		isFound=True
if not isFound:
	print("0 | Not found")

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
try:
	for channel in range(8):
		if tca[channel].try_lock():
			addresses2 = tca[channel].scan()
			isFound = False
			for address2 in addresses2:
				if(address2==0x4c):
					print("{} | 2101".format(channel+1))
					isFound=True
			if not isFound:
				print("{} | Not found".format(channel+1))
			tca[channel].unlock()
except:
        for channel in range(8):
                print("{} | Not found".format(channel+1))
