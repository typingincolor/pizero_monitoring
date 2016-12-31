#!/usr/bin/env python

import hive
import sensu
import ConfigParser, os
from blinkt import set_pixel, set_clear_on_exit, show

config = ConfigParser.RawConfigParser()
config.read(['site.cfg', os.path.expanduser('~/.pizero_monitor.cfg')])

hive_username = config.get("hive", "username")
hive_password = config.get("hive", "password")
sensu_username = config.get("sensu", "username")
sensu_password = config.get("sensu", "password")
sensu_url = config.get("sensu", "url")

hive_status, hive_data = hive.get_hive_status(hive_username, hive_password)
sensu_status, sensu_data = sensu.get_sensu_status(sensu_url, sensu_username, sensu_password)

if hive_status == 200:
    if hive_data['active']:
        set_pixel(7, 255, 0, 0, 0.05)

    r, g, b = hive.map_temperature_to_colour(hive_data['currentTemp'])
    set_pixel(6, r, g, b, 0.05)

    r, g, b = hive.map_temperature_to_colour(hive_data['outsideTemp'])
    set_pixel(5, r, g, b, 0.05)
else:
    set_pixel(7, 0, 0, 255, 0.05)
    set_pixel(6, 0, 0, 255, 0.05)
    set_pixel(5, 0, 0, 255, 0.05)

if sensu_status == 200:
    if sensu_data['critical'] == 0 and sensu_data['warning'] == 0:
        set_pixel(0, 0, 255, 0, 0.05)
        set_pixel(1, 0, 255, 0, 0.05)

    if sensu_data['warning'] > 0 and sensu_data['critical'] == 0:
        set_pixel(0, 255, 165, 0, 0.05)
        set_pixel(1, 255, 165, 0, 0.05)

    if sensu_data['critical'] > 0:
        set_pixel(0, 255, 0, 0, 0.05)
        set_pixel(1, 255, 0, 0, 0.05)
else:
    set_pixel(0, 0, 0, 255, 0.05)
    set_pixel(1, 0, 0, 255, 0.05)

set_clear_on_exit(False)
show()
