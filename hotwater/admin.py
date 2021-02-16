from django.contrib import admin

# Register your models here.
from hotwater.models import WaterHeater, CircPump
from django.urls import reverse
from django.utils.html import format_html


@admin.register(WaterHeater)
class WaterHeaterAdmin(admin.ModelAdmin):
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


@admin.register(CircPump)
class CircPumpAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sensor_link',
        'relay_link'
    )
    fields = (
        'name',
        'description',
        'sensor',
        'relay'
    )

    def sensor_link(self, obj):
        if obj.sensor:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor.pk,)),
                               obj.sensor.pk)
        else:
            return format_html('-')

    sensor_link.short_description = 'Loop Temperature Sensor'

    def relay_link(self, obj):
        if obj.relay:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_relay_change", args=(obj.relay.pk,)),
                               obj.relay.pk)
        else:
            return format_html('-')

    relay_link.short_description = 'Pump Relay'
