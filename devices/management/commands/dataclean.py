from django.core.management.base import BaseCommand
from devices.models import *
from statistics import mean
from decimal import *
from datetime import timedelta

MAX_TEMP_MOVE = 25
MIN_TEMP = 25


class Command(BaseCommand):
    help = 'clean sensor data'

    def handle(self, *args, **options):
        sensors = TempSensor.objects.all()
        for sensor in sensors:
            if sensor.last_ts_checked:
                stime = sensor.last_ts_checked - timedelta(minutes=5)
                self.stdout.write(f"checking data for {sensor.name}: starting at {stime}")
                sdata = sensor.tempsensordata_set.filter(timestamp__gt=stime).order_by('timestamp')
            else:
                self.stdout.write(f"checking data for {sensor.name}: starting at beginning of data")
                sdata = sensor.tempsensordata_set.order_by('timestamp')
            bad = 0
            if len(sdata):
                # first pass - set any values less than MIN_TEMP to MIN_TEMP or prev
                s = sdata[0]
                if s.value < MIN_TEMP:
                    s.value = Decimal(MIN_TEMP)
                    s.save()
                for i in range(1, len(sdata)):
                    s = sdata[i]
                    if s.value < MIN_TEMP:
                        s.value = sdata[i - 1].value
                        s.save()
                if len(sdata) >= 4:
                    # initialize algorithm
                    # determine if initial value is bad
                    val = sdata[0].value
                    avgval = mean((val, sdata[1].value, sdata[2].value, sdata[3].value))
                    if abs(val - avgval) > MAX_TEMP_MOVE:
                        # bad value
                        bad += 1
                        self.stdout.write(
                            f"{sensor.name}: replacing {val} with {avgval} at index 0, timestamp {sdata[0].timestamp}")
                        sdata[0].value = avgval
                        sdata[0].save()
                for i in range(1, len(sdata)):
                    # null all clearly bad values
                    prev = sdata[i - 1].value
                    val = sdata[i].value
                    if abs(val - prev) > MAX_TEMP_MOVE:
                        bad += 1
                        self.stdout.write(
                            f"{sensor.name}: replacing {val} with {prev} at index {i}, timestamp {sdata[i].timestamp}")
                        sdata[i].value = prev
                        sdata[i].save()
                sensor.last_ts_checked = sdata[len(sdata) - 1].timestamp
                sensor.last_scan_bad = bad
                sensor.total_bad = sensor.total_bad + bad
                sensor.save()
            self.stdout.write(f"{sensor.name}: {bad} bad data points out of {len(sdata)}")
