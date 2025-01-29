from django.db import models
from django.utils import timezone

from accounts.models import Location


class Device(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True)
    config = models.JSONField(null=True)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        abstract = True

    def as_json(self):
        dself = {'attributes': {'location': self.location,
                                'name': self.name,
                                'description': self.description},
                 'id': self.id,
                 'type': 'Device',
                 'self': f"/devices/{self.name}",
                 }
        return dself
