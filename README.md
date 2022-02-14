# OctoPrint-Emc2101

This plugin allows you to control the temperature of your printer enclosure using a 4 pin PWM fan connected to an Adafruit EMC2101 fan controller/temperature sensor. This Octoprint plugin is for use with a Raspberry Pi connected to an Adafruit EMC2101 fan control board.

## Hardware

This plugin controls an Adafruit EMC2101 board: https://www.adafruit.com/product/4808

Connect board VIN (red wire) to RPi 3V
Connect board GND (black wire) to RPi GND
Connect board SCL (yellow wire) to RPi SCL
Connect board SDA (blue wire) to RPi SDA

Connect board FAN (blue wire) to fan PWM input
Connect board TACH (green wire) to fan Tach output
Connect DC jack positive pin to Fan V+ input
Connect DC jack GND to Fan V-/GND input
Connect DC jack GND to RPi GND

<img width="835" alt="wiring" src="https://user-images.githubusercontent.com/942556/153914562-bbbe89f6-0c67-4c0a-ac8d-6ae551a8f02d.png">


## Setup

Install the Adafruit CircuitPython support for the EMC2101 board:

pip3 install adafruit-circuitpython-emc2101


Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/JeremyLaurenson/OctoPrint-Emc2101/archive/master.zip

**TODO:** Describe how to install your plugin, if more needs to be done than just installing it via pip or through
the plugin manager.

## Configuration

**TODO:** Describe your plugin's configuration options (if any).
