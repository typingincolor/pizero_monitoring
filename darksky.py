#!/usr/bin/env python

from time import sleep
from sys import exit

import ConfigParser
import os

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

import blinkt

config = ConfigParser.RawConfigParser()
config.read(['.darksky.cfg', os.path.expanduser('~/.darksky.cfg')])

# Grab your API key here: http://openweathermap.org
# List of city ID city.list.json.gz can be downloaded here http://bulk.openweathermap.org/sample/
API_KEY = config.get("darksky", "key")
LATLNG = config.get("darksky", "latlng")

url = 'https://api.darksky.net/forecast'

temp = 0


def update_weather():
    try:
        darksky = "%s/%s/%s" % (url, API_KEY, LATLNG)
        r = requests.get(url=darksky)
        temp = r.json().get('currently').get('apparentTemperature')
        temp = (temp - 32.0) / 1.8
        print("Temperature = " + str(temp) + " C")
        return temp
    except:
        print("Connection Error")


def show_graph(v):
    v *= 8

    if v < 0:
        v *= -1.0
        r, g, b = 0, 0, 255
    else:
        r, g, b = 255, 0, 0

    for x in range(7, -1, -1):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1
    blinkt.show()


def draw_thermo(temp):
    v = temp
    v /= 25
    v += (1 / 8)
    show_graph(v)


blinkt.set_brightness(0.1)
blinkt.set_clear_on_exit(False)
temp = update_weather()
draw_thermo(temp)
