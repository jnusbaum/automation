from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, re_path
from django.http import HttpResponseRedirect

# Register your models here.
from .models import Zone, Device, OneWireInterface, TempSensor, TempSensorData

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
    readonly_fields = (
        'name',
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'client_id',
        'device_actions',
    )
    fields = (
        'name',
        'description',
        'client_id',
        'device_actions',
    )
    readonly_fields = (
        'name',
        'device_actions',
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<device_name>.+)/config/$',
                self.admin_site.admin_view(self.process_config),
                name='device-config',
            ),
        ]
        return custom_urls + urls

    def device_actions(self, obj):
        return format_html('<a class="button" href="{}">Config</a>&nbsp;', reverse('admin:device-config', args=[obj.pk]),
        )

    def process_config(self, request, device_name, *args, **kwargs):
        # publish config-request to to sorrelhills/device/config-request/<device_name>
        # this will cause device config server to publish configuration
        self.message_user(request, f"Configured {device_name}")
        url = reverse(
            'admin:heating_device_change',
            args=[device_name],
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

    device_actions.short_description = 'Device Actions'
    device_actions.allow_tags = True

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
        return format_html('<a href="{}">{}</a>', reverse("admin:heating_device_change", args=(obj.device.pk,)), obj.device.pk)

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
        'zone_link',
        'interface_link',
    )

    fields = (
        'name',
        'address',
        'description',
        'zone',
        'one_wire_interface',
        'total_bad',
        'last_scan_bad',
        'last_ts_checked',
    )

    readonly_fields = (
        'name',
    )

    def zone_link(self, obj):
        if obj.zone:
            return format_html('<a href="{}">{}</a>',
                               reverse("admin:heating_zone_change", args=(obj.zone.pk,)),
                               obj.zone.pk)
        else:
            return format_html('-')

    zone_link.short_description = 'Zone'

    def interface_link(self, obj):
        if obj.one_wire_interface:
            return format_html('<a href="{}">{}</a>',
                                reverse("admin:heating_onewireinterface_change", args=(obj.one_wire_interface.pk,)),
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
                                reverse("admin:heating_tempsensor_change", args=(obj.sensor.pk,)),
                                obj.sensor.pk)
        else:
            return format_html('-')

    sensor_link.short_description = 'Sensor'