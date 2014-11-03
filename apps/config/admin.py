from django.contrib import admin
from .models import Server, Group, Config

admin.site.register(Server)
admin.site.register(Group)
admin.site.register(Config)
