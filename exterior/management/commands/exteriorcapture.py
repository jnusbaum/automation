from ambient_api.ambientapi import AmbientAPI
from django.core.management.base import BaseCommand
import datetime, time
import logging


logger = logging.getLogger('exteriorcapture')
logger.setLevel('INFO')


class Command(BaseCommand):
    help = 'capture exterior sensor data'

    def handle(self, *args, **options):
        api = AmbientAPI()
        devices = api.get_devices()
        device = devices[0]
        time.sleep(1)  # pause for a second to avoid API limits
        ddata = device.get_data()
        print(datetime.datetime.fromtimestamp(ddata[0]['dateutc']/1000).strftime('%Y-%m-%d %H:%M:%S'))
        print(f"outside temp = {ddata[0]['tempf']}")
        print(f"inside temp = {ddata[0]['tempinf']}")
        print(f"sunshine = {ddata[0]['solarradiation']}")
