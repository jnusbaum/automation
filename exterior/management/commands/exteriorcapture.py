from ambient_api.ambientapi import AmbientAPI
from django.core.management.base import BaseCommand
import time
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
        print(device.get_data())