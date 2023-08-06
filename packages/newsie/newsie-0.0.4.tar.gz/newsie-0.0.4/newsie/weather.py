import os
import time

from datetime import datetime, timedelta, timezone

from ambient_api.ambientapi import AmbientAPI

import newsie.config as config

def get_weather():

    weather = {}

    aapi = AmbientAPI(
        AMBIENT_ENDPOINT = config.AMBIENT_ENDPOINT,
        AMBIENT_APPLICATION_KEY = config.AMBIENT_APPLICATION_KEY,
        AMBIENT_API_KEY = config.AMBIENT_API_KEY
    )
    devices = aapi.get_devices()

    if len(devices) > 0:
        device = devices[0]
        time.sleep(1)
        device_data = device.get_data()
        current_conditions = device_data[0]

        weather = {
            "temp": current_conditions['tempf'],
            "humidity": current_conditions['humidity'],
            "pressure": current_conditions['baromrelin'],
            "windspeed": current_conditions['windspeedmph'],
            "wind_direction": current_conditions['winddir']
        }
    else:
        weather = {"temp": "69", "humidity": "0"}

    return weather
