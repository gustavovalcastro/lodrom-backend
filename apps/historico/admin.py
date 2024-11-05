from django.contrib import admin

from apps.historico.models import Historico

class Historicos(admin.ModelAdmin):
    list_display = ("id", "device_id", "get_device_code", "get_username", "event_time", "event_type")
    list_display_links = ('id', 'get_device_code',)
    list_per_page = 20

    @admin.display(description="Device Code")
    def get_device_code(self, obj):
        if obj.device_id.device_code is not None:
            return obj.device_id.device_code
        return "-"

    @admin.display(description="Account")
    def get_username(self, obj):
        if obj.account_id is not None:
            return obj.account_id.user.username
        return "-"

admin.site.register(Historico, Historicos)
