from django.db import models

from accounts.models import Location


class Collector(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    client_id = models.CharField(max_length=64, null=True)
