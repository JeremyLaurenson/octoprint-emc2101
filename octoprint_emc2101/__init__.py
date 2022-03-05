# coding=utf-8
from __future__ import absolute_import
from pickle import FALSE
import time
import random
import octoprint.plugin
import os
from octoprint.events import Events, all_events
from octoprint.util import RepeatedTimer
import sys
from subprocess import Popen, PIPE


        


class Emc2101Plugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin

):
    isDebugging = False
    isDemo = False
    sensors = []  # Array of strings with I2C channel numbers passed to the py scripts
    detecteds=[]
    fanspeeds=[]
    temperatures=[]
    targets=[]

    isInLoop=False

    def getSettingVariableName(self,channel,name):
        nameChar=chr(97+channel)
        settingName=nameChar+"_"+name
        return settingName
        
    def getSettingVariable(self,channel,name):
        nameChar=chr(97+channel)
        settingName=self.getSettingVariableName(channel,name)
        settingValue=self._settings.get([settingName])
        return settingValue
        
    def setSettingVariable(self,channel,name,settingValue):
        nameChar=chr(97+channel)
        settingName=self.getSettingVariableName(channel,name)
        self._settings.set([settingName],settingValue)

    def getChannelName(self,channel):
        channelName=self.getSettingVariable(channel,"name")
        return channelName

    def getChannelMax(self,channel):
        channelMax=self.getSettingVariable(channel,"high_temp")
        return channelMax

    def getChannelMin(self,channel):
        channelMin=self.getSettingVariable(channel,"low_temp")
        return channelMin

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        # Doing this the old fashioned way because arrays into jinja and all that are a pain in the ass.
        # Happy to take a pull request....

        use_fahrenheit= False
        a_low_temp = 23.0       # Fan A is the native i2c appearance of an EMC2101
        a_high_temp = 27.0
        a_low_fan = 20
        a_high_fan = 100
        a_name = "Default"
        a_topspeed= 1900
        
        b_low_temp = 23.0       # Fan B is the tca9548a channel 0 i2c appearance of an EMC2101
        b_high_temp = 27.0
        b_low_fan = 20
        b_high_fan = 100
        b_name = "Channel 0"
        b_topspeed= 1900
        
        
        c_low_temp = 23.0       # Fan C is the tca9548a channel 1 i2c appearance of an EMC2101
        c_high_temp = 27.0
        c_low_fan = 20
        c_high_fan = 100
        c_name = "Channel 1"
        c_topspeed= 1900
        
        d_low_temp = 23.0       # Fan D is the tca9548a channel 2 i2c appearance of an EMC2101
        d_high_temp = 27.0
        d_low_fan = 20
        d_high_fan = 100
        d_name = "Channel 2"
        d_topspeed= 1900

        e_low_temp = 23.0
        e_high_temp = 27.0
        e_low_fan = 20
        e_high_fan = 100
        e_name="Channel 3"
        e_topspeed= 1900
        
        f_low_temp = 23.0
        f_high_temp = 27.0
        f_low_fan = 20
        f_high_fan = 100
        f_name="Channel 4"
        f_topspeed= 1900
        
        g_low_temp = 23.0
        g_high_temp = 27.0
        g_low_fan = 20
        g_high_fan = 100
        g_name="Channel 5"
        g_topspeed= 1900
        
        h_low_temp = 23.0
        h_high_temp = 27.0
        h_low_fan = 20
        h_high_fan = 100
        h_name="Channel 6"
        h_topspeed= 1900
        
        i_low_temp = 23.0
        i_high_temp = 27.0
        i_low_fan = 20
        i_high_fan = 100
        i_name="Channel 7"
        i_topspeed= 1900
        
        return dict(
            use_fahrenheit=use_fahrenheit,
            a_external=False,b_external=False,c_external=False,d_external=False,e_external=False,f_external=False,
            g_external=False,h_external=False,i_external=False,
            a_low_fan=a_low_fan, a_high_fan=a_high_fan,a_low_temp=a_low_temp, a_high_temp=a_high_temp,
            b_low_fan=b_low_fan, b_high_fan=b_high_fan,b_low_temp=b_low_temp, b_high_temp=b_high_temp,
            c_low_fan=c_low_fan, c_high_fan=c_high_fan,c_low_temp=c_low_temp, c_high_temp=c_high_temp,
            d_low_fan=d_low_fan, d_high_fan=d_high_fan,d_low_temp=d_low_temp, d_high_temp=d_high_temp,
            e_low_fan=e_low_fan, e_high_fan=e_high_fan,e_low_temp=e_low_temp, e_high_temp=e_high_temp,
            f_low_fan=f_low_fan, f_high_fan=f_high_fan,f_low_temp=f_low_temp, f_high_temp=f_high_temp,
            g_low_fan=g_low_fan, g_high_fan=g_high_fan,g_low_temp=g_low_temp, g_high_temp=g_high_temp,
            h_low_fan=h_low_fan, h_high_fan=h_high_fan,h_low_temp=h_low_temp, h_high_temp=h_high_temp,
            i_low_fan=i_low_fan, i_high_fan=i_high_fan,i_low_temp=i_low_temp, i_high_temp=i_high_temp,
            a_name=a_name,b_name=b_name,c_name=c_name,d_name=d_name,e_name=e_name,f_name=f_name,g_name=g_name,h_name=h_name,i_name=i_name,
            a_topspeed=a_topspeed,b_topspeed=b_topspeed,c_topspeed=c_topspeed,d_topspeed=d_topspeed,e_topspeed=e_topspeed,
            f_topspeed=f_topspeed,g_topspeed=g_topspeed,h_topspeed=h_topspeed,i_topspeed=i_topspeed,
        )
        
    def on_after_startup(self):
        self._logger.info("EMC2101 plugin is alive!")
        self.check_emc2101()
        self.start_timer()
        


    def start_timer(self):
        if self.isDebugging:
            self._logger.info("EMC2101 timer is starting")
        timerDelay=int(len(self.sensors)*0.5) + 5
        self._check_temp_timer = RepeatedTimer(timerDelay, self.emc2101loop, None, None, True)
        self._check_temp_timer.start()



    def emc2101loop(self):
        if self.isDebugging:
            self._logger.info("EMC2101 loop")
        if self.isInLoop:
            if self.isDebugging:
                self._logger.info("EMC2101 loop aborted - already running")
            return
        self.isInLoop=True
        
        for sensor in self.sensors:
            if self.isDebugging:
                self._logger.info("Reading sensor at %s", sensor)
            prefix="a"
            if sensor=="1":
                prefix="b"
            elif sensor=="2":
                prefix="c"
            elif sensor=="3":
                prefix="d"
            elif sensor=="4":
                prefix="e"
            elif sensor=="5":
                prefix="f"
            elif sensor=="6":
                prefix="g"
            elif sensor=="7":
                prefix="h"
            elif sensor=="8":
                prefix="i"
            
            low_temp=self.tofloat(self._settings.get([prefix + "_low_temp"]))
            high_temp=self.tofloat(self._settings.get([prefix + "_high_temp"]))
            low_fan=self.toint(self._settings.get([prefix + "_low_fan"]))
            high_fan=self.toint(self._settings.get([prefix + "_high_fan"]))
            external_sensor=self.tofloat(self._settings.get([prefix + "_external"]))
            
            if self.isDebugging:
                self._logger.info("Temperature for low fan speed is %f and temperature for high fan speed is %f" % (low_temp,high_temp))
                self._logger.info("Low fan speed is %d and high fan speed is %d" % (low_fan,high_fan))
            if external_sensor:
                temp, fans = self.read_emc2101(sensor,1)
            else:
                temp, fans = self.read_emc2101(sensor,0)

            self.fanspeeds[int(sensor)]=fans
            self.temperatures[int(sensor)]=temp
            
            if self.isDebugging:
                self._logger.info("Temperature is %f and actual fan speed is %f" % (temp,fans))
            try:
                if low_temp<high_temp:
                    calculated_speed = int(((temp - low_temp) * (high_fan - low_fan) / (high_temp - low_temp)) + low_fan)
                if low_temp>=high_temp:
                    calculated_speed = int(((temp - low_temp) * (high_fan - low_fan) * -1 / (low_temp - high_temp)) + low_fan)
            except:
                calculated_speed = 0
            if calculated_speed>100:
                calculated_speed=100
            self.targets[int(sensor)]=calculated_speed
            if self.isDebugging:
                self._logger.info("Calculated fan speed is %d" % calculated_speed)
            temp, fans = self.write_emc2101(sensor,calculated_speed)

            
        self._plugin_manager.send_plugin_message(self._identifier,
                                                 dict(
                                                     use_fahrenheit=self._settings.get(["use_fahrenheit"]),
                                                     a_low_temp=self._settings.get(["a_low_temp"]),
                                                     a_high_temp=self._settings.get(["a_high_temp"]),
                                                     b_low_temp=self._settings.get(["b_low_temp"]),
                                                     b_high_temp=self._settings.get(["b_high_temp"]),
                                                     c_low_temp=self._settings.get(["c_low_temp"]),
                                                     c_high_temp=self._settings.get(["c_high_temp"]),
                                                     d_low_temp=self._settings.get(["d_low_temp"]),
                                                     d_high_temp=self._settings.get(["d_high_temp"]),
                                                     e_low_temp=self._settings.get(["e_low_temp"]),
                                                     e_high_temp=self._settings.get(["e_high_temp"]),
                                                     f_low_temp=self._settings.get(["f_low_temp"]),
                                                     f_high_temp=self._settings.get(["f_high_temp"]),
                                                     g_low_temp=self._settings.get(["g_low_temp"]),
                                                     g_high_temp=self._settings.get(["g_high_temp"]),
                                                     h_low_temp=self._settings.get(["h_low_temp"]),
                                                     h_high_temp=self._settings.get(["h_high_temp"]),
                                                     i_low_temp=self._settings.get(["i_low_temp"]),
                                                     i_high_temp=self._settings.get(["i_high_temp"]),
                                                     
                                                     a_name=self._settings.get(["a_name"]),
                                                     b_name=self._settings.get(["b_name"]),
                                                     c_name=self._settings.get(["c_name"]),
                                                     d_name=self._settings.get(["d_name"]),
                                                     e_name=self._settings.get(["e_name"]),
                                                     f_name=self._settings.get(["f_name"]),
                                                     g_name=self._settings.get(["g_name"]),
                                                     h_name=self._settings.get(["h_name"]),
                                                     i_name=self._settings.get(["i_name"]),
                                                     a_topspeed=self._settings.get(["a_topspeed"]),
                                                     b_topspeed=self._settings.get(["b_topspeed"]),
                                                     c_topspeed=self._settings.get(["c_topspeed"]),
                                                     d_topspeed=self._settings.get(["d_topspeed"]),
                                                     e_topspeed=self._settings.get(["e_topspeed"]),
                                                     f_topspeed=self._settings.get(["f_topspeed"]),
                                                     g_topspeed=self._settings.get(["g_topspeed"]),
                                                     h_topspeed=self._settings.get(["h_topspeed"]),
                                                     i_topspeed=self._settings.get(["i_topspeed"]),
                                                     a_detected=self.detecteds[0],
                                                     a_temp=self.temperatures[0],
                                                     a_fanspeed=self.fanspeeds[0],
                                                     a_target=self.targets[0],
                                                     b_detected=self.detecteds[1],
                                                     b_temp=self.temperatures[1],
                                                     b_fanspeed=self.fanspeeds[1],
                                                     b_target=self.targets[1],
                                                     c_detected=self.detecteds[2],
                                                     c_temp=self.temperatures[2],
                                                     c_fanspeed=self.fanspeeds[2],
                                                     c_target=self.targets[2],
                                                     d_detected=self.detecteds[3],
                                                     d_temp=self.temperatures[3],
                                                     d_fanspeed=self.fanspeeds[3],
                                                     d_target=self.targets[3],
                                                     e_detected=self.detecteds[4],
                                                     e_temp=self.temperatures[4],
                                                     e_fanspeed=self.fanspeeds[4],
                                                     e_target=self.targets[4],
                                                     f_detected=self.detecteds[5],
                                                     f_temp=self.temperatures[5],
                                                     f_fanspeed=self.fanspeeds[5],
                                                     f_target=self.targets[5],
                                                     g_detected=self.detecteds[6],
                                                     g_temp=self.temperatures[6],
                                                     g_fanspeed=self.fanspeeds[6],
                                                     g_target=self.targets[6],
                                                     h_detected=self.detecteds[7],
                                                     h_temp=self.temperatures[7],
                                                     h_fanspeed=self.fanspeeds[7],
                                                     h_target=self.targets[7],
                                                     i_detected=self.detecteds[8],
                                                     i_temp=self.temperatures[8],
                                                     i_fanspeed=self.fanspeeds[8],
                                                     i_target=self.targets[8]
                                                      )
        )
        self.isInLoop=False

        
        

    @staticmethod
    def tofloat(value):
        try:
            val = float(value)
            return val
        except:
            return 0

    @staticmethod
    def toint(value):
        try:
            val = int(value)
            return val
        except:
            return 0

    def check_emc2101(self):
        if self.isDebugging:
            self._logger.info("Checking for EMC2101 sensors....")
        try:
            self.sensors=[]
            self.detecteds=[]
            self.fanspeeds=[]
            self.temperatures=[]
            self.targets=[]
            script = os.path.dirname(os.path.realpath(__file__)) + "/EMCSCAN.py"
            cmd = [sys.executable, script]
            stdout = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, errors = stdout.communicate()
            if len(errors) > 0:
                self._logger.info("EMC2101 error: %s", errors)
            self._settings.set(["a_detected"], 0)
            self._settings.set(["b_detected"], 0)
            self._settings.set(["c_detected"], 0)
            self._settings.set(["d_detected"], 0)
            self._settings.set(["e_detected"], 0)
            self._settings.set(["f_detected"], 0)
            self._settings.set(["g_detected"], 0)
            self._settings.set(["h_detected"], 0)
            self._settings.set(["i_detected"], 0)
            temp_sensors = output.split("\n")
            for sensor in temp_sensors:
                if sensor.find("|")>0:
                    channel, channelstatus = sensor.split("|")
                    channelstatus=channelstatus.strip()
                    channel=channel.strip()
                    currentSensorFound=False
                    if(self.isDemo):
                        channelstatus="2101"

                    if channelstatus=="2101":
                        currentSensorFound=True
                        self._logger.info("EMC2101 crontroller number %s is connected" , channel)
                        self.sensors.append(channel)
                        if channel=="0":
                            self._settings.set(["a_detected"], 1)
                        elif channel=="1":
                            self._settings.set(["b_detected"], 1)
                        elif channel=="2":
                            self._settings.set(["c_detected"], 1)
                        elif channel=="3":
                            self._settings.set(["d_detected"], 1)
                        elif channel=="4":
                            self._settings.set(["e_detected"], 1)
                        elif channel=="5":
                            self._settings.set(["f_detected"], 1)
                        elif channel=="6":
                            self._settings.set(["g_detected"], 1)
                        elif channel=="7":
                            self._settings.set(["h_detected"], 1)
                        elif channel=="8":
                            self._settings.set(["i_detected"], 1)
                    else:
                        self._logger.info("EMC2101 controller number %s has no controller connected",channel)
                if(currentSensorFound):
                    self.detecteds.append(1)
                    self.fanspeeds.append(0)
                    self.targets.append(0)
                    self.temperatures.append(0)
                else:
                    self.detecteds.append(0)
                    self.fanspeeds.append(-1)
                    self.targets.append(-1)
                    self.temperatures.append(-1)

                
            return
        except Exception as ex:
            print(ex)
            self._logger.info(
                "Failed to execute EMC2101 python subscript...")
            return (0, 0)

    def read_emc2101(self,sensor,external_sensor):
        if self.isDebugging:
            self._logger.info("Reading current values from EMC2101 sensors....")
            if self.isDemo:
                fansDemo = self.tofloat(random.randint(400, 1700))
                tempDemo = self.tofloat(random.randint(23, 28))
                return tempDemo, fansDemo    
        try:
            script = os.path.dirname(os.path.realpath(__file__)) + "/EMC2101.py"
            cmd = [sys.executable, script, str(sensor), str(external_sensor)]
            stdout = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, errors = stdout.communicate()
            if len(errors) > 0:
                self._logger.info("EMC2101 error: %s", errors)
            temp, fans = output.split("|")
            return (self.tofloat(temp.strip()),self.tofloat(fans.strip()))
        except Exception as ex:
            print(ex)
            self._logger.info(
                "Failed to execute EMC2101 python subscript...")
            self.log_error(ex)
            return (0, 0)

    def write_emc2101(self,sensor,speed):
        if(speed>100):
            speed=100
        if(speed<0):
            speed=0
        if self.isDebugging:
            self._logger.info("Setting EMC2101 %s fan speed to %d...." % (sensor,speed))
        if self.isDemo:
            return (0,0)
        try:
            script = os.path.dirname(os.path.realpath(__file__)) + "/SETEMC2101.py"
            cmd = [sys.executable, script, sensor, str(speed)]
            stdout = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, errors = stdout.communicate()
            if len(errors) > 0:
                self._logger.info("EMC2101 error: %s", errors)
            temp, fans = output.split("|")
            return (self.tofloat(temp.strip()),self.tofloat(fans.strip()))
        except Exception as ex:
            print(ex)
            self._logger.info(
                "Failed to execute EMC2101 python subscript...")
            self.log_error(ex)
            return (0, 0)


    def on_shutdown(self):
        self._logger.info("Stopping fan monitor")
        
    def on_event(self,event, payload):
        if event == "PrintStarted":
            self._logger.info("A print has started. Uploading settings to EMC2101")
        if event == "PrintFailed":
            self._logger.info("A print has failed. Resetting EMC2101")
        if event == "PrintDone":
            self._logger.info("A print is done. Resetting EMC2101")
            
    def get_settings_version(self):
        return 3

    def on_settings_migrate(self, target, current=None):
        self._logger.warn("######### current settings version %s target settings version %s #########", current, target)

            



    def get_template_configs(self):
        return [
            dict(type="tab", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]
    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/emc2101.js"],
            "css": ["css/emc2101.css"],
            "less": ["less/emc2101.less"]
        }


    def get_graph_data(self, comm, parsed_temps):
        for sensorNum in range(9):
            temps = self.temperatures[sensorNum]
            if temps>0:
                sensorName=self.getChannelName(sensorNum)
                sensorMax=self.getChannelMax(sensorNum)  # get the max and min values so we can show the 'target'
                sensorMin=self.getChannelMin(sensorNum)  # We get min in case the particualr fan is bringing in hot air to heat the chamber
                if(sensorMin>sensorMax):
                    sensorMax=sensorMin
                parsed_temps[sensorName] = (temps, sensorMax)
        return parsed_temps

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "emc2101": {
                "displayName": "Emc2101 Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "JeremyLaurenson",
                "repo": "OctoPrint-Emc2101",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/JeremyLaurenson/OctoPrint-Emc2101/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Fan Control (EMC2101)"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3



def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Emc2101Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
	    "octoprint.comm.protocol.temperatures.received": (__plugin_implementation__.get_graph_data, 1)
    }
