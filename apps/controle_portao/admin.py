from django.contrib import admin

from apps.controle_portao.models import Portao

class Portoes(admin.ModelAdmin):
    list_display = ("id","get_account_name","get_device_code")
    list_display_links = ('id', 'get_account_name')
    list_per_page = 20
    search_fields = ('device_id__device_code','account_id__user__username',)

    @admin.display(description="Device Code")
    def get_device_code(self, obj):
        return obj.device_id.device_code

    @admin.display(description="Conta")
    def get_account_name(self, obj):
        return obj.account_id.user.username

admin.site.register(Portao, Portoes)
