from django.contrib import admin

from .models import Network


class NetworkAdmin(admin.ModelAdmin):
    fields = ['name', 'ipv4_cidr', 'vid', 'note']
    search_fields = ['ipv4_cidr']


admin.site.register(Network, NetworkAdmin)
