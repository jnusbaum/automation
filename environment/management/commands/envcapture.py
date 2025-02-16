from ambient_api.ambientapi import AmbientAPI
from django.conf import settings
from django.core.management.base import BaseCommand
from environment.models import EnvSensorData
from django.db.utils import OperationalError
import time
import logging


logger = logging.getLogger('envcapture')
logger.setLevel('INFO')


class Command(BaseCommand):
    help = 'capture sensor data'

    def handle(self, *args, **options):
        api = AmbientAPI()
        devices = api.get_devices()
        device = devices[0]
        time.sleep(1)  # pause for a second to avoid API limits
        print(device.get_data())
