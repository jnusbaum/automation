from django.contrib import admin

# Register your models here.
from heating.models import Zone

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
