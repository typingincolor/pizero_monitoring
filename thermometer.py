#!/usr/bin/env python

#Data from OpenWeatherMap
#show_graph function adapted from cpu_temp.py

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
config.read(['.thermometer.cfg', os.path.expanduser('~/.thermometer.cfg')])

#Grab your API key here: http://openweathermap.org
#List of city ID city.list.json.gz can be downloaded here http://bulk.openweathermap.org/sample/
API_KEY=config.get("openweathermap.org", "key")
CITY_ID=config.get("openweathermap.org", "city_id")

url = 'http://api.openweathermap.org/data/2.5/weather'

temp = 0

def update_weather():
    payload = {
        'id': CITY_ID,
        'units': 'metric',
        'appid': API_KEY
    }
    global temp
    try:
        r = requests.get(url=url, params=payload)
        temp = r.json().get('main').get('temp')
        print("Temperture = "+str(temp)+" C")
    except:
        print("Connection Error")

def show_graph(v, r, g, b):
    v *= 8
    for x in range(8):
        if v  < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v,1.0) * c) for c in [r,g,b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1
    blinkt.show()

def draw_thermo(temp):
    v = temp
    v /= 40
    v += (1/8)
    show_graph(v, 255, 0, 0)

blinkt.set_brightness(0.1)

update_weather()
draw_thermo(temp)
