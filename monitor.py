#!/usr/bin/env python

import hive
import sensu
import argparse
from blinkt import set_pixel, set_clear_on_exit, show

parser = argparse.ArgumentParser()
parser.add_argument("--hive-username", type=str, help="hive username", required=True)
parser.add_argument("--hive-password", type=str, help="hive password", required=True)
parser.add_argument("--sensu-api-username", type=str, help="sensu api username", required=True)
parser.add_argument("--sensu-api-password", type=str, help="sensu api password", required=True)
parser.add_argument("--sensu-api-url", type=str, help="sensu api url", required=True)

args = parser.parse_args()

active, currentTemp, targetTemp = hive.get_hive_status(args.hive_username, args.hive_password)
warning, critical = sensu.get_sensu_status(args.sensu_api_url, args.sensu_api_username, args.sensu_api_password)

if active:
    set_pixel(7, 255, 0, 0, 0.05)

r,g,b=hive.rgb(12, 23, currentTemp)
set_pixel(6, r, g, b, 0.05)

if critical == 0 and warning == 0:
    set_pixel(0, 0, 255, 0, 0.05)
    set_pixel(1, 0, 255, 0, 0.05)

if warning > 0 and critical == 0:
    set_pixel(0, 255, 165, 0, 0.05)
    set_pixel(1, 255, 165, 0, 0.05)

if critical > 0:
    set_pixel(0, 255, 0, 0, 0.05)
    set_pixel(1, 255, 0, 0, 0.05)

set_clear_on_exit(False)
show()