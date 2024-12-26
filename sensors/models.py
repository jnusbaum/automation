from django.db import models
from collectors.models import Collector
from devices.models import Device
from django.utils import timezone


class Sensor(models.Model):
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    config = models.JSONField()


class OneWireInterface(models.Model):
    description = models.CharField(max_length=512, null=True)
    pin_number = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "OneWireInterface"
        verbose_name_plural = "OneWireInterfaces"

    def as_json(self, altvalue=None):
        dself = {'attributes': {'description': self.description,
                                'pin_number': self.pin_number},
                 'id': self.id,
                 'type': 'OneWireInterface',
                 'self': f"/onewireinterfaces/{self.id}",
                 'relationships': {'device': f"/devices/{self.device.name}"}
                 }
        return dself

class TempSensor(Sensor):
    one_wire_interface = models.ForeignKey(OneWireInterface, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=512, null=True)
    total_bad = models.IntegerField(default=0)
    last_scan_bad = models.IntegerField(default=0)
    last_ts_checked = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "TempSensor"
        verbose_name_plural = "TempSensors"

    def as_json(self):
        dself = {'attributes': {'address': self.address,
                                'description': self.description,
                                'total_bad': self.total_bad,
                                'last_scan_bad': self.last_scan_bad,
                                'last_ts_checked': self.last_ts_checked},
                 'id': self.name,
                 'type': 'TempSensor',
                 'self': f"/devices/{self.name}",
                 'relationships': {'data': f"/tempsensors/{self.name}/data/",
                                   'interface': f"/onewireinterfaces/{self.one_wire_interface.id}/" if self.one_wire_interface else '',
                                   },
                 }
        return dself

class TempSensorData(models.Model):
    sensor = models.ForeignKey(TempSensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    original_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.sensor_id}:{self.timestamp}"

    class Meta:
        verbose_name = "TempSensorData"
        verbose_name_plural = "TempSensorData"
        indexes = [
            models.Index(fields=['sensor', '-timestamp'], name='devices_tsensordata_sid_ts'),
        ]

    def as_json(self):
        dself = {'attributes': {'timestamp': round(self.timestamp.timestamp() * 1000),
                                'value': self.value,
                                'original_value': self.original_value},
                 'id': self.id,
                 'type': 'TempSensorData',
                 'self': f"/tempsensors/{self.sensor.name}/data/{self.id}/",
                 'relationships': {'sensor': f"/tempsensors/{self.sensor.name}/"}
                 }
        return dself

