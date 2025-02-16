from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html


from devices.models import Device, DeviceStatus


@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    # list_display = (
    #     'id',
    #     'timestamp',
    #     'status',
    #     'device_link',
    # )
    #
    # fields = ('id',
    #           'timestamp',
    #           'status',
    #           'device'
    #           )
    #
    # readonly_fields = (
    #     'id',
    #     'timestamp',
    #     'device'
    # )
    #
    # def device_link(self, obj):
    #     if obj.device:
    #         return format_html('<a href="{}">{}</a>',
    #                            reverse("admin:devices_device_change", args=(obj.device.pk,)),
    #                            obj.device.pk)
    #     else:
    #         return format_html('-')
    #
    # device_link.short_description = 'Device'
    pass
