# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import sqlite3
import os
from subprocess import Popen
from octoprint.events import Events, all_events



class Emc2101Plugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin

):

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        targettemp=23
        fanSpeed0=20
        fanSpeed1=30
        fanSpeed2=40
        fanSpeed3=50
        fanSpeed4=60
        fanSpeed5=80
        fanSpeed6=100
        fanSpeed7=100
        minutestokeep=-60
        interval = 10
        return dict(targettemp=targettemp, interval=interval, minutestokeep=minutestokeep,fanspeed0=fanSpeed0,fanspeed1=fanSpeed1,fanspeed2=fanSpeed2,fanspeed3=fanSpeed3,fanspeed4=fanSpeed4,fanspeed5=fanSpeed5,fanspeed6=fanSpeed6,fanspeed7=fanSpeed7)
        
    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        emc2101_path = self.get_plugin_data_folder();
        sqlFileName=emc2101_path + "/emc2101.db"
        conn = sqlite3.connect(sqlFileName)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('target_temp','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["targettemp"]),self._settings.get(["targettemp"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed0','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed0"]),self._settings.get(["fanspeed0"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed1','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed1"]),self._settings.get(["fanspeed1"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed2','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed2"]),self._settings.get(["fanspeed2"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed3','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed3"]),self._settings.get(["fanspeed3"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed4','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed4"]),self._settings.get(["fanspeed4"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed5','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed5"]),self._settings.get(["fanspeed5"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed6','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed6"]),self._settings.get(["fanspeed6"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('fanspeed7','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["fanspeed7"]),self._settings.get(["fanspeed7"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('interval','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["interval"]),self._settings.get(["interval"]))
        conn.execute(sql)
        sql="INSERT INTO settings (settingName, settingValue) VALUES ('historylines','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (self._settings.get(["minutestokeep"]),self._settings.get(["minutestokeep"]))
        conn.execute(sql)
        conn.commit()
        conn.close()
        
        
    def on_settings_load(self):
        emc2101_path = self.get_plugin_data_folder()
        sqlFileName=emc2101_path + "/emc2101.db"
        conn = sqlite3.connect(sqlFileName)
        sql="SELECT settingName,settingValue from settings"
        cursor = conn.execute(sql)
        targettemp=23
        fanSpeed0=20
        fanSpeed1=30
        fanSpeed2=40
        fanSpeed3=50
        fanSpeed4=60
        fanSpeed5=80
        fanSpeed6=100
        fanSpeed7=100
        minutestokeep=-60
        interval = 10
        for row in cursor:
           settingName=row[0]
           settingValue=row[1]
           if settingName=="target_temp":
                targettemp=int(settingValue)
           if settingName=="interval":
                interval=int(settingValue)
           if settingName=="fanspeed0":
                fanSpeed0=int(settingValue)
           if settingName=="fanspeed1":
                fanSpeed1=int(settingValue)
           if settingName=="fanspeed2":
                fanSpeed2=int(settingValue)
           if settingName=="fanspeed3":
                fanSpeed3=int(settingValue)
           if settingName=="fanspeed4":
                fanSpeed4=int(settingValue)
           if settingName=="fanspeed5":
                fanSpeed5=int(settingValue)
           if settingName=="fanspeed6":
                fanSpeed6=int(settingValue)
           if settingName=="fanspeed7":
                fanSpeed7=int(settingValue)
           if settingName=="interval":
                interval=int(settingValue)
           if settingName=="historylines":
               minutestokeep=int(settingValue)
        conn.close()
        self._logger.info("Loaded settings: Target Temp is %d" % targettemp)
        if minutestokeep<1:
           minutestokeep=minutestokeep*-1
        return dict(targettemp=targettemp, interval=interval, minutestokeep=minutestokeep,fanspeed0=fanSpeed0,fanspeed1=fanSpeed1,fanspeed2=fanSpeed2,fanspeed3=fanSpeed3,fanspeed4=fanSpeed4,fanspeed5=fanSpeed5,fanspeed6=fanSpeed6,fanspeed7=fanSpeed7)

    def on_after_startup(self):
        self._logger.info("EMC2101 plugin is alive!")
        path = os.path.dirname(os.path.abspath(__file__))
        tempControlScript=path + "/tempcontrol.py"
        self._logger.info("Launching fan monitor %s" % tempControlScript)
        emc2101_path = self.get_plugin_data_folder();
        sqlFileName=emc2101_path + "/emc2101.db"
        p = Popen(['python', tempControlScript, sqlFileName])

    def on_shutdown(self):
        self._logger.info("Stopping fan monitor")
        p.terminate()
        
    def on_event(self,event, payload):
        if event == "PrintStarted":
            self._logger.info("A print has started. Uploading settings to EMC2101")
        if event == "PrintFailed":
            self._logger.info("A print has failed. Resetting EMC2101")
        if event == "PrintDone":
            self._logger.info("A print is done. Resetting EMC2101")
            
        
    def get_template_configs(self):
        return [
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
__plugin_name__ = "EMC2101 Fan Control"

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
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
