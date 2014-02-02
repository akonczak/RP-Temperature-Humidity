#!/usr/bin/python

###############################################################################
#
#
# Methods to help retrieve information about temperature and humidity.
#
#
###############################################################################

import subprocess
import re
import datetime
from time import *
import sys
from FileStorage import writeRow
from modules import lcddriver


sensorLib = "resources/Adafruit_DHT"
dataPath = "data/temperature-humidity.csv"


###############################################################################
#
#
#   Read date from sensor,
#   We can't read directly from sensor python is to slow for that.
#   Instead of that we are using program written in C++ and we will parse response,
#   to get information about temperature and humidity
#
#
###############################################################################
def readSensorOneTime(GPIO):
    output = subprocess.check_output([sensorLib, "2302", GPIO])
    matches1 = re.search("Temp =\s+([0-9.]+)", output)
    matches2 = re.search("Hum =\s+([0-9.]+)", output)

    if not matches1 and not matches2:
        raise ValueError("Unable to read data")

    temperature = float(matches1.group(1))
    humidity = float(matches2.group(1))
    return temperature, humidity


###############################################################################
#
#
#   Smart way to get single result from sensor
#
#
###############################################################################
def readSensor(GPIO):
    while True:
        try:
            return readSensorOneTime(GPIO)
        except ValueError as e:
            print e
            sleep(3)



###############################################################################
#
#
#   Main loop reading constantly sensor
#
#
###############################################################################
print "start"
lcd = lcddriver.lcd(0x27, 0)
waitXTimes = 5
counter = 0

while True:

    dateAndTime = datetime.datetime.now()
    row = []

    row.append("17")
    sensor1 = readSensor("17")
    row.append(sensor1[0])
    row.append(sensor1[1])
#    sleep(1)
#    row.append("18")
#    sensor2 = readSensor("18")
#    row.append(sensor2[0])
#    row.append(sensor2[1])

    try:

        #write data to file only once per 5 mins
        if counter == 0:
            writeRow(dataPath, dateAndTime, row)

        lcd.lcd_display_string(str(dateAndTime), 1)
        lcd.lcd_display_string("T=" + str(sensor1[0]) + " H=" + str(sensor1[1]), 2)
        counter = waitXTimes

        #lcd.lcd_display_string("T=" + str(sensor2[0]) + " H=" + str(sensor2[1]), 2)

    except IOError as er:
        print "Unable to append data " + er
        #wait 5s and try again
        sleep(5)
        #sys.exit()

    # Wait 60 seconds before continuing
    sleep(60)
    counter -= 1
