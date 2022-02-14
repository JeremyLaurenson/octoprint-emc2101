# OctoPrint-Emc2101

This plugin allows you to control the temperature of your printer enclosure using a 4 pin PWM fan connected to an Adafruit EMC2101 fan controller/temperature sensor. This Octoprint plugin is for use with a Raspberry Pi connected to an Adafruit EMC2101 fan control board:

![4808-04](https://user-images.githubusercontent.com/942556/153941335-980945da-9b34-45c7-8ad6-9cf4f0ef874e.jpg)


## Hardware

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


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/JeremyLaurenson/OctoPrint-Emc2101/archive/master.zip

**TODO:** Describe how to install your plugin, if more needs to be done than just installing it via pip or through
the plugin manager.

## Configuration

**TODO:** Describe your plugin's configuration options (if any).
