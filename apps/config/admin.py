from django.contrib import admin
from .models import Server, Group, Config
from django.conf.urls import patterns
from django.shortcuts import get_object_or_404

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

def set_enable_transfer(modeladmin, request, queryset):
    queryset.update(enable_transfer=True)
set_enable_transfer.short_description = u"Enable transfer on selected items"

def set_disable_transfer(modeladmin, request, queryset):
    queryset.update(enable_transfer=False)
set_disable_transfer.short_description = u"Disable transfer on selected items"

def set_enable_reload(modeladmin, request, queryset):
    queryset.update(enable_reload=True)
set_enable_reload.short_description = u"Enable reload on selected items"

def set_disable_reload(modeladmin, request, queryset):
    queryset.update(enable_reload=False)
set_disable_reload.short_description = u"Disable reload on selected items"

class ConfigDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class ServerAdmin(ConfigDefaultAdmin):
    list_display = [ 'name', 'address', 'enabled' ]
    fields = [ 'name', 'address', 'ssh_user', 'ssh_password', 'ssh_port', 'enabled' ]

class GroupAdmin(ConfigDefaultAdmin):
    fields = [ 'name', 'enabled' ]
    list_display = [ 'name', 'enabled' ]

class ConfigAdmin(ConfigDefaultAdmin):
    actions = [set_enable_transfer,set_disable_transfer,set_enable_reload,set_disable_reload]
    fields = [ 'group', 'temp_dir', 'nginx_maps_dir', 'nginx_conf_dir', 'nginx_sites_dir', 'ldirectord_conf', 'varnish_dir', 'cluster_servers', 'enable_transfer', 'enable_reload', 'enabled' ]
    list_display = [ 'group', 'enable_transfer', 'enable_reload', 'enabled' , 'enable_link']

    def get_urls(self):
        urls = super(ConfigAdmin, self).get_urls()
        my_urls = patterns('', 
            (r'^enable/(?P<pk>\d+)/$', self.set_enable)
        )
        return my_urls + urls

    def set_enable(self, request):
        obj = get_object_or_404(Config, pk=pk)
        obj.enable=True
        obj.save()

admin.site.register(Server, ServerAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Config, ConfigAdmin)
