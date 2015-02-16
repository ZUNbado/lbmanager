from django.contrib import admin
from .models import Member, Cluster
from ..config.models import Server

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

class ClusterDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class MemberAdmin(ClusterDefaultAdmin):
    fields = ('server', 'port', 'ssl_port', 'enabled')
    list_display = ('server', 'port', 'ssl_port', 'enabled')

    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['server'].queryset = Server.objects.filter(role_cluster=True).exclude(id__in=[m.server.id for m in Member.objects.all().exclude(pk=obj.pk)])
        else:
            form.base_fields['server'].queryset = Server.objects.filter(role_cluster=True).exclude(id__in=[m.server.id for m in Member.objects.all()])
        return form

class ClusterAdmin(ClusterDefaultAdmin):
    list_display = ('name', 'address', 'port', 'ssl', 'ssl_port', 'enabled')
    fieldsets = (
        (None, {
            'fields': ('name', 'backends', 'address', 'port', 'mode', 'ssl', 'ssl_port', 'enabled')
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
