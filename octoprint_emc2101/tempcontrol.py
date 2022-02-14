# Additional code by Jeremy Laurenson
from datetime import datetime
import time
import board
from adafruit_emc2101.emc2101_lut import EMC2101_LUT as EMC2101
import sqlite3
import os

emc2101_path = "/home/pi/.octoprint/data/emc2101"
isExist = os.path.exists(emc2101_path)
if not isExist:
  os.makedirs(emc2101_path)
sqlFileName=emc2101_path + "/emc2101.db"

minutes_to_keep=-60
interval = 10
fanSpeed0=20
fanSpeed1=30
fanSpeed2=40
fanSpeed3=50
fanSpeed4=60
fanSpeed5=70
fanSpeed6=80
fanSpeed7=100


i2c = board.I2C()  # uses board.SCL and board.SDA
FAN_MAX_RPM = 1700
emc = EMC2101(i2c)
print("Internal temperature:", emc.internal_temperature, "C")
print("Currently running at %f RPM:" % emc.fan_speed)


def database_connect():
    conn = sqlite3.connect(sqlFileName)
    conn.execute('''CREATE TABLE IF NOT EXISTS `sensorlog` ( `logDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , `instance` INT NOT NULL DEFAULT '1' , `temperature` REAL NOT NULL , `targetTemperature` REAL NOT NULL , `targetCycle` INT NOT NULL , `fanSpeed` REAL NOT NULL );''')
    conn.commit()
    conn.execute('''CREATE TABLE IF NOT EXISTS `settings`  ( `settingName` VARCHAR(20) NOT NULL PRIMARY KEY , `settingValue` VARCHAR(20) NOT NULL);''')

    conn.close()

def log_sensors(instance,temperature,targetTemp,targetCycle,fanSpeed):
    conn = sqlite3.connect(sqlFileName)
    sql="INSERT INTO sensorlog (instance,temperature,targetTemperature,targetCycle,fanSpeed) VALUES (%d,%f,%f,%d,%f)" % (instance,temperature,targetTemp,targetCycle,fanSpeed)
    conn.execute(sql)
    conn.commit()
    sql="DELETE FROM sensorlog WHERE logDate  <= datetime('now','%d minute')" % minutes_to_keep
    conn.execute(sql)
    conn.commit()
    conn.close()

def get_settings():
    global targettemp
    global minutes_to_keep
    global interval
    global fanSpeed0
    global fanSpeed1
    global fanSpeed2
    global fanSpeed3
    global fanSpeed4
    global fanSpeed5
    global fanSpeed6
    global fanSpeed7

    targettemp=25
    fanSpeed0=20
    fanSpeed1=30
    fanSpeed2=40
    fanSpeed3=50
    fanSpeed4=60
    fanSpeed5=80
    fanSpeed6=100
    fanSpeed7=100

    conn = sqlite3.connect(sqlFileName)
    sql="SELECT settingName,settingValue from settings"
    cursor = conn.execute(sql)
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
            minutes_to_keep=int(settingValue)
    conn.close()
    if minutes_to_keep>0:
       minutes_to_keep=minutes_to_keep * -1

def get_setting(settingName,defValue):
    conn = sqlite3.connect(sqlFileName)
    settingValue=defValue
    sql="SELECT settingValue from settings where settingName='%s'" % settingName
    cursor = conn.execute(sql)
    for row in cursor:
       settingValue=row[0]
    return settingValue
    conn.close()

def set_setting(settingName,settingValue):
    conn = sqlite3.connect(sqlFileName)
    sql="INSERT INTO settings (settingName, settingValue) VALUES ('%s','%s') ON CONFLICT(settingName) DO UPDATE SET settingValue='%s'" % (settingName,settingValue,settingValue)
    conn.execute(sql)
    conn.commit()
    conn.close()


database_connect()

while True:
    get_settings()
    print("****Target temperature from config is %d****" % targettemp)
    print("Fan speeds: %d %d %d %d %d %d %d %d" % (fanSpeed0,fanSpeed1,fanSpeed2,fanSpeed3,fanSpeed4,fanSpeed5,fanSpeed6,fanSpeed7))
    print("Update interval is %d seconds, and %d minutes of data is saved in the database" % (interval,minutes_to_keep*-1))
    print("Internal temperature:", emc.internal_temperature, "C")
    target_fan_speed=fanSpeed0
    recorded_temp=emc.internal_temperature
    overtemp= recorded_temp - targettemp
    print("Currently we are over temperature by ",overtemp)
    if overtemp > 0:
        target_fan_speed=fanSpeed1
        if overtemp>1:
            target_fan_speed=fanSpeed2
        if overtemp>2:
            target_fan_speed=fanSpeed3
        if overtemp>3:
            target_fan_speed=fanSpeed4
        if overtemp>4:
            target_fan_speed=fanSpeed5
        if overtemp>5:
            target_fan_speed=fanSpeed6
        if overtemp>6:
            target_fan_speed=fanSpeed7

    print("Fan speed target ",target_fan_speed)
    emc.manual_fan_speed = target_fan_speed
    print("Currently running at %f RPM" % emc.fan_speed)
    log_sensors(1,recorded_temp,targettemp,target_fan_speed,emc.fan_speed)
    time.sleep(interval)
