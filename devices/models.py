from django.db import models
from django.utils import timezone


class Device(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=512)
    client_id = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    def as_json(self):
        dself = {'attributes': {'description': self.description,
                                'client_id': self.client_id},
                 'id': self.name,
                 'type': 'Device',
                 'self': f"/devices/{self.name}",
                 'relationships': {'devices': f"/devices/device/{self.name}"}
                 }
        return dself


class DeviceStatus(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.device_id}:{self.timestamp}"

    class Meta:
        verbose_name = "DeviceStatus"
        verbose_name_plural = "DeviceStatus"
        indexes = [
            models.Index(fields=['device', '-timestamp'], name='sensors_device_sid_ts'),
        ]

    def as_json(self):
        dself = {'attributes': {'timestamp': round(self.timestamp.timestamp() * 1000),
                                'status': self.status,
                                },
                 'id': self.id,
                 'type': 'DeviceStatus',
                 'self': f"automation/devices/api/devices/{self.device.name}/data/{self.id}",
                 'relationships': {'relay': f"automation/devices/api/devices/{self.device.name}"}
                 }
        return dself


class OneWireInterface(models.Model):
    description = models.CharField(max_length=512)
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
                 'self': f"automation/devices/api/onewireinterfaces/{self.id}",
                 'relationships': {'device': f"automation/devices/api/devices/{self.device.name}"}
                 }
        return dself


class TempSensor(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    one_wire_interface = models.ForeignKey(OneWireInterface, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=512)
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
                 'relationships': {'data': f"/devices/{self.name}/data",
                                   'device': f"/devices/{self.one_wire_interface.device.name}"}
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
            models.Index(fields=['sensor', '-timestamp'], name='heating_tsensordata_sid_ts'),
        ]

    def as_json(self):
        dself = {'attributes': {'timestamp': round(self.timestamp.timestamp() * 1000),
                                'value': self.value,
                                'original_value': self.original_value},
                 'id': self.id,
                 'type': 'TempSensorData',
                 'self': f"/devices/{self.sensor.name}/data/{self.id}",
                 'relationships': {'sensor': f"/devices/{self.sensor.name}"}
                 }
        return dself


class Relay(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    pin_number = models.IntegerField()
    description = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Relay"
        verbose_name_plural = "Relays"

    def as_json(self):
        dself = {'attributes': {'description': self.description,
                                'pin_number': self.pin_number},
                 'id': self.name,
                 'type': 'Relay',
                 'self': f"/relays/{self.name}",
                 'relationships': {'device': f"/devices/{self.device.name}"}
                 }
        return dself


class RelayData(models.Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.BooleanField()

    def __str__(self):
        return f"{self.relay_id}:{self.timestamp}"

    class Meta:
        verbose_name = "RelayData"
        verbose_name_plural = "RelayData"
        indexes = [
            models.Index(fields=['relay', '-timestamp'], name='sensors_relay_sid_ts'),
        ]

    def as_json(self):
        dself = {'attributes': {'timestamp': round(self.timestamp.timestamp() * 1000),
                                'value': self.value,
                                },
                 'id': self.id,
                 'type': 'RelayData',
                 'self': f"/relays/{self.relay.name}/data/{self.id}",
                 'relationships': {'relay': f"/relays/{self.relay.name}"}
                 }
        return dself
