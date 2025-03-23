import time

from ambient_api.ambientapi import AmbientAPI
from django.core.management.base import BaseCommand
import logging
from datetime import datetime, timezone
from devices.models import TempSensorData, WindSensorData, SunSensorData
from weather.models import Weather
from django.db import OperationalError, IntegrityError
import os


logger = logging.getLogger('weathercapture')
logger.setLevel('DEBUG')
os.environ['AMBIENT_ENDPOINT'] = 'https://rt.ambientweather.net/v1'
os.environ['AMBIENT_API_KEY'] = '2ec9e80358ec4b5b80bbeb6d009071d3c3cb3f856d604c4cb94227277cada3f6'
os.environ['AMBIENT_APPLICATION_KEY'] = 'ba1d0b43b3644aa884d2769fdf7d0a8ac9828765b0ec4d6aa16e547b706dac08'


class Command(BaseCommand):
    help = 'capture weather sensor data'

    def handle(self, *args, **options):
        # run in cron on a 5 minute cycle
        weather = Weather.objects.get(pk='OUTSIDE')
        api = AmbientAPI()
        devices = api.get_devices()
        device = devices[0]
        # sleep for a second to avoid throttling
        time.sleep(1)
        while True:
            ddata = device.get_data()
            data = ddata[0]
            timestamp = datetime.fromtimestamp(timestamp=data['dateutc']/1000, tz=timezone.utc)
            received_timestamp = datetime.now(tz=timezone.utc)

            tdata = TempSensorData(sensor=weather.sensor_temp,
                                   timestamp=timestamp,
                                   value=data['tempf'],
                                   original_value=data['tempf'],
                                   received_timestamp=received_timestamp
                                   )
            try:
                tdata.save()
            except OperationalError:
                # log error but continue
                logger.error(f"error - db locked")
            except IntegrityError:
                # duplicate timestamp, ignore
                logger.warning(f"warning - duplicate sensor, timestamp")
            else:
                logger.debug(f"saved data for sensor = {weather.sensor_temp.name}")

            wdata = WindSensorData(sensor=weather.sensor_wind,
                                   timestamp=timestamp,
                                   value=data['windspeedmph'],
                                   received_timestamp=received_timestamp
                                   )
            try:
                wdata.save()
            except OperationalError:
                # log error but continue
                logger.error(f"error - db locked")
            except IntegrityError:
                # duplicate timestamp, ignore
                logger.warning(f"warning - duplicate sensor, timestamp")
            else:
                logger.debug(f"saved data for sensor = {weather.sensor_wind.name}")

            sdata = SunSensorData(sensor=weather.sensor_sun,
                                  timestamp=timestamp,
                                  value=data['solarradiation'],
                                  received_timestamp=received_timestamp
                                  )
            try:
                sdata.save()
            except OperationalError:
                # log error but continue
                logger.error(f"error - db locked")
            except IntegrityError:
                # duplicate timestamp, ignore
                logger.warning(f"warning - duplicate sensor, timestamp")
            else:
                logger.debug(f"saved data for sensor = {weather.sensor_sun.name}")

            # wait 5 minutes
            time.sleep(300)


