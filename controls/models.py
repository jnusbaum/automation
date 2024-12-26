from django.db import models
from django.utils import timezone
from devices.models import Device


class Control(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    pass


class Relay(Control):
    pin_number = models.IntegerField()
    description = models.CharField(max_length=512, null=True)

    class Meta:
        verbose_name = "Relay"
        verbose_name_plural = "Relays"

    def as_json(self):
        dself = {'attributes': {'description': self.description,
                                'pin_number': self.pin_number},
                 'id': self.name,
                 'type': 'Relay',
                 'self': f"/relays/{self.name}",
                 'relationships': {'device': f"/devices/{self.device.name}/"}
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
                 'self': f"/relays/{self.relay.name}/data/{self.id}/",
                 'relationships': {'relay': f"/relays/{self.relay.name}/"}
                 }
        return dself
