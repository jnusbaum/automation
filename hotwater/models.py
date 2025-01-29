from django.db import models

from accounts.models import Location
from devices.models import Device
from sensors.models import TempSensor
from controls.models import Relay


class WaterHeater(Device):
    sensor_in = models.ForeignKey(TempSensor, related_name='sensor_in', on_delete=models.RESTRICT)
    sensor_out = models.ForeignKey(TempSensor, related_name='sensor_out', on_delete=models.RESTRICT)
    sensor_burn = models.ForeignKey(TempSensor, related_name='sensor_burn', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "WaterHeater"
        verbose_name_plural = "WaterHeaters"

    def as_json(self):
        dself: dict[str, str | dict[str, str | Location] | int] = super().as_json()
        dself['type'] = 'WaterHeater'
        dself['self'] = f"/waterheaters/{self.sensor.name}"
        dself['relationships'] = {
            'sensor_in': f"automation/sensors/api/tempsensors/{self.sensor_in.name}",
            'sensor_out': f"automation/sensors/api/tempsensors/{self.sensor_out.name}",
            'sensor_burn': f"automation/sensors/api/tempsensors/{self.sensor_burn.name}"
        }
        return dself


class CircPump(Device):
    sensor = models.ForeignKey(TempSensor, related_name='sensor', on_delete=models.RESTRICT)
    relay = models.OneToOneField(Relay, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "CircPump"
        verbose_name_plural = "CircPumps"

    def as_json(self):
        dself: dict[str, str | dict[str, str | Location] | int] = super().as_json()
        dself['type'] = 'CircPump'
        dself['self'] = f"/circpumps/{self.sensor.name}"
        dself['relationships'] = {
            'sensor': f"automation/sensors/api/tempsensors/{self.sensor.name}",
            'relay': f"automation/controls/api/relays/{self.relay.name}"
        }
        return dself
