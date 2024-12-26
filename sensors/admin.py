from django.contrib import admin
from .models import OneWireInterface, Sensor, TempSensor, TempSensorData
from django.urls import reverse


@admin.register(OneWireInterface)
class OneWireInterfaceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'description',
        'pin_number',
        'device_link',
    )
    fields = (
        'id',
        'description',
        'pin_number',
        'device',
    )
    readonly_fields = (
        'id',
    )

    def device_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:devices_device_change", args=(obj.device.pk,)),
                           obj.device.pk)

    device_link.short_description = 'Device'


@admin.register(TempSensor)
class TempSensorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'description',
        'total_bad',
        'last_scan_bad',
        'last_ts_checked',
        'interface_link',
    )

    fields = (
        'name',
        'address',
        'description',
        'one_wire_interface',
        'total_bad',
        'last_scan_bad',
        'last_ts_checked',
    )

    def interface_link(self, obj):
        if obj.one_wire_interface:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_onewireinterface_change", args=(obj.one_wire_interface.pk,)),
                               obj.one_wire_interface.description)
        else:
            return format_html('-')

    interface_link.short_description = 'Interface'


@admin.register(TempSensorData)
class TempSensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'value',
        'original_value',
        'sensor_link',
    )

    fields = ('id',
              'timestamp',
              'value',
              'original_value',
              'sensor',)

    readonly_fields = (
        'id',
        'timestamp',
        'sensor',
    )

    def sensor_link(self, obj):
        if obj.sensor:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_tempsensor_change", args=(obj.sensor.pk,)),
                               obj.sensor.pk)
        else:
            return format_html('-')

    sensor_link.short_description = 'Sensor'