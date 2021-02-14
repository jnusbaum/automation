from django.db import models
from sensors.models import TempSensor, Relay


class WaterHeater(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensor_in = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_out = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_burn = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "WaterHeater"
        verbose_name_plural = "WaterHeaters"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'WaterHeater',
                 'self': f"/zones/{self.name}",
                 'relationships': {'sensor_in': f"/sensors/zone/{self.name}"}
                 }
        return dself


class CircPump(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensor = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    relay = models.OneToOneField(Relay, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "CircPump"
        verbose_name_plural = "CircPumpss"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'CircPump',
                 'self': f"/circpumps/{self.name}",
                 'relationships': {'sensors': f"/sensors/zone/{self.name}"}
                 }
        return dself