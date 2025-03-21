from django.db import models
from django.utils import timezone
from devices.models import TempSensor, WindSensor, SunSensor


class Weather(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512, null=True)
    sensor_temp = models.OneToOneField(TempSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_wind = models.OneToOneField(WindSensor, related_name='+', on_delete=models.RESTRICT)
    sensor_sun = models.OneToOneField(SunSensor, related_name='+', on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Weather"
        verbose_name_plural = "Weathers"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'type': 'Weather',
                 'self': f"/weathers/{self.name}",
                 'relationships': {'sensor_temp': f"/devices/{self.sensor_temp.name}",
                                   'sensor_wind': f"/devices/{self.sensor_wind.name}",
                                   'sensor_sun': f"/devices/{self.sensor_sun.name}",
                                   }
                 }
        return dself
