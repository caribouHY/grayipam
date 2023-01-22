from django.contrib import admin

from .models import Network, Host


class NetworkAdmin(admin.ModelAdmin):
    fields = ['name', 'vid', 'note']
    search_fields = ['ipv4_cidr']


class HostAdmin(admin.ModelAdmin):
    fields = ['network', 'hostname', 'ipv4']
    search_fields = ['hostname', 'ipv4']


admin.site.register(Network, NetworkAdmin)
admin.site.register(Host, HostAdmin)
