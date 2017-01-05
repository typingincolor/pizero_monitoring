#!/usr/bin/env python

import ConfigParser
import os
import struct

import sensu
from blinkt import set_pixel, set_clear_on_exit, show

config = ConfigParser.RawConfigParser()
config.read(['.pizero_monitor.cfg', os.path.expanduser('~/.pizero_monitor.cfg')])


def pixel(px, hexcolour):
    colour = struct.unpack('BBB', hexcolour.decode('hex'))
    set_pixel(px, colour[0], colour[1], colour[2], 0.05)

sensu_username = config.get("sensu", "username")
sensu_password = config.get("sensu", "password")
sensu_url = config.get("sensu", "url")

critical = config.get("colour", "critical")
warning = config.get("colour", "warning")
ok = config.get("colour", "ok")
unknown = config.get("colour", "unknown")

sensu_status, sensu_data = sensu.get_sensu_status(sensu_url, sensu_username, sensu_password)

if sensu_status == 200:
    if sensu_data['critical'] == 0 and sensu_data['warning'] == 0:
        pixel(7, ok)

    if sensu_data['warning'] > 0 and sensu_data['critical'] == 0:
        pixel(7, warning)

    if sensu_data['critical'] > 0:
        pixel(7, critical)
else:
    pixel(7, unknown)

set_clear_on_exit(False)
show()
