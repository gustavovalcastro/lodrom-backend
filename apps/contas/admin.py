from django.contrib import admin

from apps.contas.models import Conta

class Contas(admin.ModelAdmin):
    list_display = ("id","get_username","user_type","device_id")
    list_display_links = ('id', 'get_username',)
    list_per_page = 20
    search_fields = ('get_username',)

    @admin.display(description="Username")
    def get_username(self, obj):
        return obj.user.username

admin.site.register(Conta, Contas)
