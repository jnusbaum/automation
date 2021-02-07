from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from sensors.models import Device, OneWireInterface, TempSensor, TempSensorData, Relay, RelayData


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'client_id',
        # 'device_actions',
    )
    fields = (
        'name',
        'description',
        'client_id',
        # 'device_actions',
    )


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
        return format_html('<a href="{}">{}</a>', reverse("admin:sensors_device_change", args=(obj.device.pk,)),
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
                               reverse("admin:sensors_onewireinterface_change", args=(obj.one_wire_interface.pk,)),
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
              'sensor_link',)

    readonly_fields = (
        'id',
        'timestamp',
        'sensor_link',
    )

    def sensor_link(self, obj):
        if obj.sensor:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:sensors_tempsensor_change", args=(obj.sensor.pk,)),
                               obj.sensor.pk)
        else:
            return format_html('-')

    sensor_link.short_description = 'Sensor'


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'device',
        'pin_number',
        'description',
    )

    fields = (
        'name',
        'device',
        'pin_number',
        'description',
    )


@admin.register(RelayData)
class RelayDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'value',
        'relay_link',
    )

    fields = ('id',
              'timestamp',
              'value',
              'relay_link',)

    readonly_fields = (
        'id',
        'timestamp',
        'relay_link',
    )

    def relay_link(self, obj):
        if obj.relay:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:sensors_relay_change", args=(obj.relay.pk,)),
                               obj.relay.pk)
        else:
            return format_html('-')

    relay_link.short_description = 'Relay'
