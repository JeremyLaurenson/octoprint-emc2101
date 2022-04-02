import sys
import time
import board
import adafruit_emc2101
import adafruit_tca9548a
import adafruit_mcp9808

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

if len(sys.argv) == 3:
	channel = int(sys.argv[1])
	internal = int(sys.argv[2])
else:
	print('-1 | -1')
	sys.exit(1)

try:
	if(channel==0):
		emc = adafruit_emc2101.EMC2101(i2c)
	else:
		emc = adafruit_emc2101.EMC2101(tca[channel-1])

	itemperature = emc.internal_temperature
	etemperature = emc.external_temperature
	fanspeed = emc.fan_speed

	if internal==0:
		temperature=itemperature
	else:
		temperature=etemperature
except:
	fanspeed=-1


try:
	if(channel==0):
		mcp = adafruit_mcp9808.MCP9808(i2c)
	else:
		mcp = adafruit_mcp9808.MCP9808(tca[channel-1])
	temperature = mcp.temperature
except:
	nomcp=1


	
print('{0:0.1f} | {1:0.1f}'.format(temperature, fanspeed))


