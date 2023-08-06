#!/usr/bin/env python

import sys
from climatempopy import ClimaTempo
from aiohttp import ClientSession
import asyncio

'''
To call this script:
$ pip3 install climatempopy
$ get_weather_georeferenced YOUR_CLIMATEMPO_TOKEN LAT LON 
'''

your_climatempo_token = str(sys.argv[1])
lat = str(sys.argv[2])
lon = str(sys.argv[3])

async def main():
    async with ClientSession() as session:
        climatempo = ClimaTempo(session, your_climatempo_token)
        climatempo.set_locale_id_from_coords(lat,lon)
        climatempo.update_current_weather()
        climatempo.update_72_hours_forecast()
        climatempo.update_15_days_forecast()
    print(climatempo.current)
    print(climatempo.forecast_72_hours)
    print(climatempo.forecast_15_days)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())