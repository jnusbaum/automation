from django.db import models
from sensors.models import TempSensor, Relay


class WaterHeater(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensors = models.ManyToManyField(TempSensor)

    class Meta:
        verbose_name = "WaterHeater"
        verbose_name_plural = "WaterHeaters"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'WaterHeater',
                 'self': f"/zones/{self.name}",
                 'relationships': {'sensors': f"/sensors/zone/{self.name}"}
                 }
        return dself


class CircPump(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensor = models.OneToOneField(TempSensor)
    relay = models.OneToOneField(Relay)

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