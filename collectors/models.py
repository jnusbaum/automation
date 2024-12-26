from django.db import models

from accounts.models import Location


# Create your models here.
class Collector(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=64, null=True)
