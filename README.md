# OctoPrint-Emc2101

This plugin uses Adafruit STEMMA QT / Qwiic based boards to allow you to easily connect up to 9 temperature sensors and/or fan controllers to your Raspberry Pi in order to control  your printer enclosure with zero soldering.

* Raspberry Pi Hat: https://www.adafruit.com/product/5142
* Cables to connect them: https://www.adafruit.com/?q=STEMMA+QT+CABLE&sort=BestMatch
* Combo Fan Controller+Temp Sensors: https://www.adafruit.com/product/4808
* High Accuracy Temp Sensors: https://www.adafruit.com/product/5027
* 8 Port Mux: https://www.adafruit.com/product/4704


<img width="635" alt="Screen Shot 2022-03-05 at 11 08 22 AM" src="https://user-images.githubusercontent.com/942556/156891679-1196be1e-3088-4a72-9509-f33ac88fe568.png">
<img width="503" alt="Screen Shot 2022-03-19 at 8 53 05 AM" src="https://user-images.githubusercontent.com/942556/159121896-3c51a58e-b3ab-46f2-a8f8-d976e4c07d84.png">
<img width="639" alt="Screen Shot 2022-03-05 at 11 08 15 AM" src="https://user-images.githubusercontent.com/942556/156891682-f5da3b3b-6f8a-4bcc-b7db-86351d9884b5.png">


This Octoprint plugin is for use with a Raspberry Pi connected to an Adafruit EMC2101 fan control board in simple mode:

![4808-04](https://user-images.githubusercontent.com/942556/153941335-980945da-9b34-45c7-8ad6-9cf4f0ef874e.jpg)


## Basic Hardware

This plugin controls an Adafruit EMC2101 board: https://www.adafruit.com/product/4808

<img width="1586" alt="pcb" src="https://user-images.githubusercontent.com/942556/153915344-50ffb32f-8c90-438d-971e-3a94299c0e5f.png">

Board to Raspberry Pi Connections:

*Connect Adafruit EMC2101 board VIN (red wire) to Raspberry Pi 3V pin
*Connect Adafruit EMC2101 board GND (black wire) to Raspberry Pi  GND
*Connect Adafruit EMC2101 board SCL - Serial Clock - (yellow wire) to Raspberry Pi  SCL
*Connect Adafruit EMC2101 board SDA - Serial Data - (blue wire) to Raspberry Pi SDA

Board to 4 Pin PWM Fan connections:

*Connect board FAN (blue wire) to fan PWM input
*Connect board TACH (green wire) to fan Tach output

Fan Power connections:
*Connect the fan power source positive to Fan V+ input
*Connect the fan power source ground to Fan V-/GND input
*Connect the fan power source ground to Raspberry Pi GND


## Multi Fan Hardware

*It is very important to wire up the MUX and Controllers exactly as shown. When I tried to dasiy chain and that sort of thing, it did not work.*

This plugin controls up to 8 Adafruit EMC2101 boards: https://www.adafruit.com/product/4808
using a SparkFun or Adafruit TCA9548A Mux: https://www.adafruit.com/product/4704

<img width="1441" alt="complex" src="https://user-images.githubusercontent.com/942556/156375979-ad8ebc42-c544-4533-b826-59aba207b0a5.png">

The internal temperature sensor is accturate to 1 degree but does not report back any finer detail than 1 degree. You may want to use an external temperature sensor diode if you want to make this more accurate or place the temp sensor exactly where you want it.

The board's DN and DP are for the diode Negative and Positive terminals respectively. Using a 2n3904 Transistor connected you can get more than just the one degree steps from the 2101 as shown below. You can find detail on what diodes to use and their accuracy on the 2101 site here: https://www.microchip.com/en-us/product/EMC2101#document-table
![IMG_5148](https://user-images.githubusercontent.com/942556/156886487-61b599d4-0292-47cd-8a91-a2482b7a3715.JPG)


![adafruit_products_image-2](https://user-images.githubusercontent.com/942556/156385413-2f590e8b-5562-4ff7-904a-1fd2e1a2f65a.png)


## Adding Adafruit MCP9808 Precision I2C Temperature Sensor

The 9808 Temperature sensor is a more accurate sensor still than the external 2101 sensor. It's accuracy is 0.25°C over -40°C to 125°C range (0.5°C guaranteed max from -20°C to 100°C)
In order to use this sensor, simply plug it onto the 2101 as a daisy chained device, or put it in standalone if you dont need the fan speed:

![adafruit_products_MCP9808_top_header](https://user-images.githubusercontent.com/942556/161259560-eb5da03f-7464-44bc-a2fd-af1fc0d59790.jpg)

<img width="721" alt="Screen Shot 2022-04-01 at 8 08 19 AM" src="https://user-images.githubusercontent.com/942556/161260408-51b612e4-ddd2-49b4-a196-1afcb537a52d.png">


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/JeremyLaurenson/OctoPrint-Emc2101/archive/main.zip



## Configuration

Each EMC2101 reports back temperature and fan speed, and can be set to whatever power you need.


<img width="445" alt="Screen Shot 2022-03-02 at 9 11 16 AM" src="https://user-images.githubusercontent.com/942556/156377836-94a77d7a-f8d4-4e86-99a7-67c4564bc5c1.png">


## Tab View

<img width="637" alt="Screen Shot 2022-03-02 at 9 12 41 AM" src="https://user-images.githubusercontent.com/942556/156378092-0074fa3b-1d5d-4f73-80a9-2c546e1ceedd.png">


