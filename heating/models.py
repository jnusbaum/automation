from django.db import models
from django.utils import timezone


# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    type = models.CharField(max_length=8, choices=[('TEMP', 'Temperature'), ('POS', 'Position'), ('ONOFF', 'On/Off')])
    address = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

class SensorData(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value_real = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    value_bool = models.BooleanField(null=True)

    class Meta:
        verbose_name = "SensorData"
        verbose_name_plural = "SensorData"