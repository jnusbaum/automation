from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from heating.models import Zone, Boiler, MixingValve


@admin.register(Boiler)
class BoilerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor_in_link',
        'sensor_out_link',
        'sensor_burn_link'
    )
    fields = (
        'name',
        'description',
        'sensor_in',
        'sensor_out',
        'sensor_burn'
    )

    def sensor_in_link(self, obj):
        if obj.sensor_in:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_in.pk,)),
                               obj.sensor_in.pk)
        else:
            return format_html('-')

    sensor_in_link.short_description = 'Input Sensor'

    def sensor_out_link(self, obj):
        if obj.sensor_out:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_out.pk,)),
                               obj.sensor_out.pk)
        else:
            return format_html('-')

    sensor_out_link.short_description = 'Output Sensor'

    def sensor_burn_link(self, obj):
        if obj.sensor_burn:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_burn.pk,)),
                               obj.sensor_burn.pk)
        else:
            return format_html('-')

    sensor_burn_link.short_description = 'Burner Sensor'


@admin.register(MixingValve)
class MixingValveAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor_sys_in_link',
        'sensor_out_link',
        'sensor_boiler_in_link'
    )
    fields = (
        'name',
        'description',
        'sensor_sys_in',
        'sensor_out',
        'sensor_boiler_in'
    )

    def sensor_sys_in_link(self, obj):
        if obj.sensor_sys_in:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_sys_in.pk,)),
                               obj.sensor_sys_in.pk)
        else:
            return format_html('-')

    sensor_sys_in_link.short_description = 'System Input Sensor'

    def sensor_out_link(self, obj):
        if obj.sensor_out:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_out.pk,)),
                               obj.sensor_out.pk)
        else:
            return format_html('-')

    sensor_out_link.short_description = 'Output Sensor'

    def sensor_boiler_in_link(self, obj):
        if obj.sensor_boiler_in:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor_boiler_in.pk,)),
                               obj.sensor_boiler_in.pk)
        else:
            return format_html('-')

    sensor_boiler_in_link.short_description = 'Boiler Input Sensor'


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
