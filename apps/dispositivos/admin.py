from django.contrib import admin

from apps.dispositivos.models import Dispositivo

class Dispositivos(admin.ModelAdmin):
    list_display = ("id","user_type","device_code")
    list_display_links = ('id', 'device_code',)
    list_per_page = 20
    search_fields = ('device_code',)

admin.site.register(Dispositivo, Dispositivos)
