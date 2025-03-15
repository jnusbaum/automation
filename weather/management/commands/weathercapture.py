from ambient_api.ambientapi import AmbientAPI
from django.core.management.base import BaseCommand
import datetime, time
import logging

from devices.models import TempSensorData, WindSensorData, SunSensorData
from weather.models import Weather
from django.db import OperationalError
import os


logger = logging.getLogger('weathercapture')
logger.setLevel('DEBUG')
os.environ['AMBIENT_ENDPOINT'] = 'https://rt.ambientweather.net/v1'
os.environ['AMBIENT_API_KEY'] = '2ec9e80358ec4b5b80bbeb6d009071d3c3cb3f856d604c4cb94227277cada3f6'
os.environ['AMBIENT_APPLICATION_KEY'] = 'ba1d0b43b3644aa884d2769fdf7d0a8ac9828765b0ec4d6aa16e547b706dac08'


class Command(BaseCommand):
    help = 'capture weather sensor data'

    def handle(self, *args, **options):
        api = AmbientAPI()
        devices = api.get_devices()
        device = devices[0]
        time.sleep(1)  # pause for a second to avoid API limits
        ddata = device.get_data()
        timestamp = datetime.datetime.fromtimestamp(ddata[0]['dateutc']/1000)
        data = ddata[0]

        weather = Weather.objects.get(pk='OUTSIDE')
        tdata = TempSensorData(sensor=weather.sensor_temp,
                               timestamp=timestamp,
                               value=data['tempf'],
                               original_value=data['tempf']
                               )
        try:
            tdata.save()
        except OperationalError:
            # db locked
            logger.error(f"error - db locked")
        except KeyError:
            # duplicate
            pass
        except ValueError:
            # bad value
            logger.error(f"error - bad value for temperature")

        wdata = WindSensorData(sensor=weather.sensor_wind,
                               timestamp=timestamp,
                               value=data['windspeedmph']
                               )
        try:
            wdata.save()
        except OperationalError:
            # db locked
            logger.error(f"error - db locked")
        except KeyError:
            # duplicate
            pass
        except ValueError:
            # bad value
            logger.error(f"error - bad value for wind")

        sdata = SunSensorData(sensor=weather.sensor_sun,
                              timestamp=timestamp,
                              value=data['solarradiation']
                              )
        try:
            sdata.save()
        except OperationalError:
            # db locked
            logger.error(f"error - db locked")
        except KeyError:
            # duplicate
            pass
        except ValueError:
            # bad value
            logger.error(f"error - bad value for sunshine")


