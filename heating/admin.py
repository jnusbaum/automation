from django.contrib import admin

# Register your models here.
from .models import Zone, Device, OneWireInterface, TempSensor, TempSensorData

admin.site.register(Zone)
admin.site.register(Device)
admin.site.register(OneWireInterface)
admin.site.register(TempSensor)
admin.site.register(TempSensorData)
