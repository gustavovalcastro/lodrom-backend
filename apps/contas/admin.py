from django.contrib import admin

from apps.contas.models import Conta

class Contas(admin.ModelAdmin):
    list_display = ("id","user__username","user_type","device_id")
    list_display_links = ('id', 'user__username',)
    list_per_page = 20
    search_fields = ('user__username',)

admin.site.register(Conta, Contas)
