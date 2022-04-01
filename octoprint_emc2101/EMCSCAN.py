from sre_constants import NOT_LITERAL
import time
import board
import adafruit_tca9548a
import adafruit_emc2101
import adafruit_mcp9808

i2c = board.I2C()  # uses board.SCL and board.SDA
addresses = i2c.scan()
isFound=False
print("0", end = '')
foundEMC=False
foundMCP=False

for address in addresses:
	if(address==0x4c):
		foundEMC=True
	if(address==0x18):
		foundMCP=True
if (foundEMC and foundMCP):
	print(" | 2101+9808")
if (foundEMC and (not foundMCP)):
	print(" | 2101")
if ((not foundEMC) and foundMCP):
        print(" | 9808")
if ((not foundEMC) and (not foundMCP)):
        print(" | Not found")

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
try:
	for channel in range(8):
		if tca[channel].try_lock():
			addresses2 = tca[channel].scan()
			foundEMC = False
			foundMCP = False
			print("{} ".format(channel+1), end = '')
			for address2 in addresses2:
				if(address2==0x4c):
					foundEMC=True
				if(address2==0x18):
					foundMCP=True
			tca[channel].unlock()
			if (foundEMC and foundMCP):
			        print(" | 2101+9808")
			if (foundEMC and (not foundMCP)):
			        print(" | 2101")
			if ((not foundEMC) and foundMCP):
			        print(" | 9808")
			if ((not foundEMC) and (not foundMCP)):
			        print(" | Not found")
except:
        for channel in range(8):
                print("{} | Not found | Not found".format(channel+1))
