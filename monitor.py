#!/usr/bin/env python

import ConfigParser
import os
import struct

import hive
import sensu
from blinkt import set_pixel, set_clear_on_exit, show

config = ConfigParser.RawConfigParser()
config.read(['site.cfg', os.path.expanduser('~/.pizero_monitor.cfg')])


def pixel(px, hexcolour):
    colour = struct.unpack('BBB', hexcolour.decode('hex'))
    set_pixel(px, colour[0], colour[1], colour[2], 0.05)


hive_username = config.get("hive", "username")
hive_password = config.get("hive", "password")
sensu_username = config.get("sensu", "username")
sensu_password = config.get("sensu", "password")
sensu_url = config.get("sensu", "url")

critical = config.get("colour", "critical")
warning = config.get("colour", "warning")
ok = config.get("colour", "ok")
unknown = config.get("colour", "unknown")

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
    pixel(7, unknown)
    pixel(6, unknown)
    pixel(5, unknown)

if sensu_status == 200:
    if sensu_data['critical'] == 0 and sensu_data['warning'] == 0:
        pixel(0, ok)
        pixel(1, ok)

    if sensu_data['warning'] > 0 and sensu_data['critical'] == 0:
        pixel(0, warning)
        pixel(1, warning)

    if sensu_data['critical'] > 0:
        pixel(0, critical)
        pixel(1, critical)
else:
    pixel(0, unknown)
    pixel(1, unknown)

set_clear_on_exit(False)
show()
