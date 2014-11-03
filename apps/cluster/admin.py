from django.contrib import admin
from .models import Member, Cluster

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

class MemberAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]
    fields = ('server', 'port', 'enabled')
    list_display = ('server', 'port', 'enabled')

class ClusterAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]
    list_display = ('name', 'address', 'port', 'group', 'enabled')
    fieldsets = (
        (None, {
            'fields': ('name', 'backends', 'group', 'address', 'port', 'mode', 'enabled')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('scheduler', 'persistent', 'netmask', 'protocol')
        }),
        ('Fallback options', {
            'classes': ('collapse',),
            'fields': ('fallback_ip', 'fallback_port')
        })
    )

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Member, MemberAdmin)
