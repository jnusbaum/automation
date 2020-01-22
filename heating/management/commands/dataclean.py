from django.core.management.base import BaseCommand
from heating.models import *
from statistics import mean
from decimal import *

MAX_TEMP_MOVE = 25
MIN_TEMP = 30

class Command(BaseCommand):
    help = 'clean sensor data'

    def handle(self, *args, **options):
        sensors = Sensor.objects.all()
        for sensor in sensors:
            if sensor.last_ts_checked:
                sdata = sensor.sensordata_set.filter(timestamp__gt=sensor.last_ts_checked).order_by('-timestamp')
            else:
                sdata = sensor.sensordata_set.order_by('-timestamp')
            bad = 0
            if len(sdata):
                if len(sdata) >= 4:
                    # initialize algorithm
                    # determine if initial value is bad
                    val = sdata[0].value
                    avgval = mean((val, sdata[1].value, sdata[2].value, sdata[3].value))
                    if val < MIN_TEMP or abs(val - avgval) > MAX_TEMP_MOVE:
                        # bad value
                        bad += 1
                        self.stdout.write(f"{sensor.name}: replacing {val} with {avgval} at index 0, timestamp {sdata[0].timestamp}")
                        sdata[0].value = avgval
                        sdata[0].save()
                else:
                    val = sdata[0].value
                    if val < MIN_TEMP:
                        bad += 1
                        val = Decimal(MIN_TEMP)
                        sdata[0].value = val
                        sdata[0].save()
                for i in range(1, len(sdata)):
                    # null all clearly bad values
                    prev = val
                    val = sdata[i].value
                    if val < MIN_TEMP or abs(val - prev) > MAX_TEMP_MOVE:
                        bad += 1
                        self.stdout.write(f"{sensor.name}: replacing {val} with {prev} at index {i}, timestamp {sdata[i].timestamp}")
                        val = prev
                        sdata[i].value = val
                sensor.last_ts_checked = sdata[-1].timestamp
                sensor.last_scan_bad = bad
                sensor.total_bad = sensor.total_bad + bad
                sensor.save()
            self.stdout.write(f"{sensor.name}: {bad} bad data points out of {len(sdata)}")
