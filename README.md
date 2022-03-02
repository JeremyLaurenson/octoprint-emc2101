# OctoPrint-Emc2101

This plugin allows you to control the temperature of your printer enclosure using a 4 pin PWM fan connected to an Adafruit EMC2101 fan controller/temperature sensor. This Octoprint plugin is for use with a Raspberry Pi connected to an Adafruit EMC2101 fan control board in simple mode:

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

This plugin controls up to 8 Adafruit EMC2101 boards: https://www.adafruit.com/product/4808
using a SparkFun or Adafruit TCA9548A Mux: https://www.adafruit.com/product/4704

<img width="1441" alt="complex" src="https://user-images.githubusercontent.com/942556/156375979-ad8ebc42-c544-4533-b826-59aba207b0a5.png">

The internal temperature sensor is accturate to 1 degree but does not report back any finer detail than 1 degree. You may want to use an external temperature sensor diode if you want to make this more accurate or place the temp sensor exactly where you want it.

The board's DN and DP are for the diode Negative and Positive terminals respectively. You can find detail on what diodes to use and their accuracy on the 2101 site here: https://www.microchip.com/en-us/product/EMC2101#document-table

![adafruit_products_image-2](https://user-images.githubusercontent.com/942556/156385413-2f590e8b-5562-4ff7-904a-1fd2e1a2f65a.png)


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/JeremyLaurenson/OctoPrint-Emc2101/archive/main.zip



## Configuration

Each EMC2101 reports back temperature and fan speed, and can be set to whatever power you need.


<img width="445" alt="Screen Shot 2022-03-02 at 9 11 16 AM" src="https://user-images.githubusercontent.com/942556/156377836-94a77d7a-f8d4-4e86-99a7-67c4564bc5c1.png">


## Tab View

<img width="637" alt="Screen Shot 2022-03-02 at 9 12 41 AM" src="https://user-images.githubusercontent.com/942556/156378092-0074fa3b-1d5d-4f73-80a9-2c546e1ceedd.png">


