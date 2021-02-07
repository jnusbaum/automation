from django.db import models
from sensors.models import TempSensor


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
