from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from devices.models import Device, DeviceStatus, OneWireInterface, TempSensor, TempSensorData, Relay, RelayData


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


@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'status',
        'device_link',
    )

    fields = ('id',
              'timestamp',
              'status',
              'device'
    )

    readonly_fields = (
        'id',
        'timestamp',
        'device'
    )

    def device_link(self, obj):
        if obj.device:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_device_change", args=(obj.device.pk,)),
                               obj.device.pk)
        else:
            return format_html('-')

    device_link.short_description = 'Device'


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


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'device_link',
        'pin_number',
        'description',
    )

    fields = (
        'name',
        'device',
        'pin_number',
        'description',
    )

    def device_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:devices_device_change", args=(obj.device.pk,)),
                           obj.device.pk)

    device_link.short_description = 'Device'


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
              'relay',)

    readonly_fields = (
        'id',
        'timestamp',
        'relay',
    )

    def relay_link(self, obj):
        if obj.relay:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:devices_relay_change", args=(obj.relay.pk,)),
                               obj.relay.pk)
        else:
            return format_html('-')

    relay_link.short_description = 'Relay'
