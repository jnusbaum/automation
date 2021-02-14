from django.db import models
from sensors.models import TempSensor


class Boiler(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensor_in = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_out = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_burn = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Boiler"
        verbose_name_plural = "Boilers"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'Boiler',
                 'self': f"/boilers/{self.name}",
                 'relationships': {'sensor_in': f"/sensors/{self.sensor_in.name}",
                                   'sensor_out': f"/sensors/{self.sensor_out.name}",
                                   'sensor_burn': f"/sensors/{self.sensor_burn.name}"},
                 }
        return dself


class MixingValve(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensor_sys_in = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_boiler_in = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_out = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "MixingValve"
        verbose_name_plural = "MixingValves"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'MixingValve',
                 'self': f"/mixingvalves/{self.name}",
                 'relationships': {'sensor_sys_in': f"/sensors/{self.sensor_sys_in.name}",
                                   'sensor_out': f"/sensors/{self.sensor_out.name}",
                                   'sensor_boiler_in': f"/sensors/{self.sensor_boiler_in.name}"},
                 }
        return dself


class Zone(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    sensors = models.ManyToManyField(TempSensor)

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'Zone',
                 'self': f"/zones/{self.name}",
                 'relationships': {'sensors': f"/sensors/zone/{self.name}"}
                 }
        return dself
