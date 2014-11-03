from django.contrib import admin
from .models import Backend, Director

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

class BalancerDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class BackendAdmin(BalancerDefaultAdmin):
    list_display = ('name', 'server', 'port', 'enabled')
    fieldsets = (
        (None, {
            'fields': ('name', 'server', 'port', 'enabled')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('host_header', 'connect_timeout', 'first_byte_timeout', 'between_bytes_timeout', 'max_connections')
        }),
        ('Probe options', {
            'classes': ('collapse',),
            'fields': ('probe_url', 'probe_timeout', 'probe_interval', 'probe_window', 'probe_threshold')
        })
    )

class DirectorAdmin(BalancerDefaultAdmin):
    fields = ('name', 'backends', 'dirtype', 'group', 'enabled')
    list_display = ('name', 'dirtype', 'group', 'enabled')

admin.site.register(Director, DirectorAdmin)
admin.site.register(Backend, BackendAdmin)
