from django.contrib import admin

# Register your models here.
from heating.models import Zone, Boiler, MixingValve

@admin.register(Boiler)
class BoilerAdmin(admin.ModelAdmin):
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

@admin.register(MixingValve)
class MixingValveAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor_sys_in',
        'sensor_out',
        'sensor_boiler_in'
    )
    fields = (
        'name',
        'description',
        'sensor_sys_in',
        'sensor_out',
        'sensor_boiler_in'
    )


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    fields = (
        'name',
        'description',
    )
