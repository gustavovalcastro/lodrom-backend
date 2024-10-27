from django.contrib import admin

from apps.recados.models import Recado
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta

class UsernameFilter(admin.SimpleListFilter):
    title = 'Username'
    parameter_name = 'username'

    def lookups(self, request, model_admin):
        usernames = set((recado.account_id.user.username for recado in Recado.objects.all()))
        return [(username, username) for username in usernames]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(account_id__user__username=self.value())
        return queryset

class DeviceCodeFilter(admin.SimpleListFilter):
    title = 'Device Code'
    parameter_name = 'device_code'

    def lookups(self, request, model_admin):
        device_codes = set((recado.device_id.device_code for recado in Recado.objects.all()))
        return [(code, code) for code in device_codes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(device_id__device_code=self.value())
        return queryset

class Recados(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_device_code', 'message', 'created_at', 'start_time', 'end_time', 'days_week')
    list_display_links = ('id', 'get_username', 'get_device_code', 'message',)
    list_filter = (UsernameFilter, DeviceCodeFilter)
    list_per_page = 15
    search_fields = ('message',)

    @admin.display(description="Username")
    def get_username(self, obj):
        return obj.account_id.user.username

    @admin.display(description="Device Code")
    def get_device_code(self, obj):
        return obj.device_id.device_code

admin.site.register(Recado, Recados)
