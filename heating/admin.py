from django.contrib import admin

# Register your models here.
from .models import Zone, Sensor, SensorData

admin.site.register(Zone)
admin.site.register(Sensor)
admin.site.register(SensorData)
