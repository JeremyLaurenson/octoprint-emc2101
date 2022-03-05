import sys
import time
import board
import adafruit_emc2101
import adafruit_tca9548a

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
if(channel==0):
	emc = adafruit_emc2101.EMC2101(i2c)
else:
	emc = adafruit_emc2101.EMC2101(tca[channel-1])

itemperature = emc.internal_temperature
etemperature = emc.external_temperature

if internal==0:
	temperature=itemperature
else:
	temperature=etemperature
	
fanspeed = emc.fan_speed
print('{0:0.1f} | {1:0.1f}'.format(temperature, fanspeed))
