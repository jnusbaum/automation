from django.contrib import admin

# Register your models here.
from hwcirc.models import WaterHeater, CircPump

@admin.register(WaterHeater)
class WaterHeaterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor_in',
        'sensor_out',
        'sensor_burn'
    )
    fields = (
        'name',
        'description',
        'sensor_in',
        'sensor_out',
        'sensor_burn'
    )

@admin.register(CircPump)
class CircPumpAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor',
        'relay'
    )
    fields = (
        'name',
        'description',
        'sensor',
        'relay'
    )
