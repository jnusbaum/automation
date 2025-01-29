from django.contrib import admin
from controls.models import Relay, RelayData
# from django.urls import reverse


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    # list_display = (
    #     'name',
    #     'device_link',
    #     'pin_number',
    #     'description',
    # )
    #
    # fields = (
    #     'name',
    #     'device',
    #     'pin_number',
    #     'description',
    # )
    #
    # def device_link(self, obj):
    #     return format_html('<a href="{}">{}</a>', reverse("admin:devices_device_change", args=(obj.device.pk,)),
    #                        obj.device.pk)
    #
    # device_link.short_description = 'Device'
    pass


@admin.register(RelayData)
class RelayDataAdmin(admin.ModelAdmin):
    # list_display = (
    #     'id',
    #     'timestamp',
    #     'value',
    #     'relay_link',
    # )
    #
    # fields = ('id',
    #           'timestamp',
    #           'value',
    #           'relay',)
    #
    # readonly_fields = (
    #     'id',
    #     'timestamp',
    #     'relay',
    # )
    #
    # def relay_link(self, obj):
    #     if obj.relay:
    #         return format_html('<a href="{}">{}</a>',
    #                            reverse("admin:devices_relay_change", args=(obj.relay.pk,)),
    #                            obj.relay.pk)
    #     else:
    #         return format_html('-')
    #
    # relay_link.short_description = 'Relay'
    pass
