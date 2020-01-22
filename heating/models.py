from django.db import models
from django.utils import timezone


class Zone(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"

    def as_json(self):
        dself = {'attributes': {'description': self.description},
                 'id': self.name,
                 'self': f"/zones/{self.name}",
                 'relationships': {
                     'sensors': f"/sensors/zone/{self.name}"
                 }
                 }
        return dself


class Sensor(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=8, choices=[('TEMP', 'Temperature'), ('POS', 'Position'), ('ONOFF', 'On/Off')])
    address = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

    def as_json(self):
        dself = {'attributes': {'type': self.type,
                                'address': self.address,
                                'description': self.description
                                },
                 'id': self.name,
                 'type': 'Sensor',
                 'self': f"/sensors/{self.name}",
                 'relationships': {
                     'data': f"/sensors/{self.name}/data",
                     'zone': f"/zones/{self.zone.name}" if self.zone else '',
                 }
                 }
        return dself


class SensorData(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    original_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = "SensorData"
        verbose_name_plural = "SensorData"
        indexes = [
            models.Index(fields=['sensor', '-timestamp'], name='heating_sensordata_sensor_id_timestamp'),
        ]

    def as_json(self, altvalue=None):
        dself = {'attributes': {'timestamp': self.timestamp,
                                # this is a decimal so we convert it to a string here
                                'value': altvalue if altvalue else self.value,
                                'original_value': self.original_value,
                                },
                 'id': self.id,
                 'type': 'SensorData',
                 'self': f"/sensors/{self.sensor.name}/data/{self.id}",
                 'relationships': {
                     'sensor': f"/sensors/{self.sensor.name}"
                 }
                 }
        return dself
