from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template
from django.core.urlresolvers import reverse

import os, shutil, re
from prettytable import PrettyTable
import requests

from .models import Group, Server
from ..cluster.models import Cluster, Member
from ..nginx.models import NginxVirtualHost
from ..web.models import Domain, DomainAlias, UrlRedir, HostRedir
from libs.confmanager import ConfManager, FilesManager
import utils

def sync(request):
    template = loader.get_template('database/sync.html')
    context = RequestContext(request, {
        'status' : utils.sync()
    })

    return HttpResponse(template.render(context))

def health(request):
    (grid, status) = utils.health()

    template = loader.get_template('tools/backend_health.html')
    context = RequestContext(request, {
        'grid' : grid,
        'status' : status
    })
    return HttpResponse(template.render(context))

def backend_disable(request, backend_name):
    utils.backend_set_state(backend_name, 'sick')
    return redirect(reverse('apps.config.views.health'))

def backend_enable(request, backend_name):
    utils.backend_set_state(backend_name, 'healthy')
    return redirect(reverse('apps.config.views.health'))

def database_status(request):
    group = Group.objects.get(pk=1)
    last_update = group.last_update.strftime('%s') if group.last_update else None
    last_apply = group.last_apply.strftime('%s') if group.last_apply else None
    data = { 'last_update' : last_update, 'last_apply' : last_apply, 'version' : group.version, 'last_update_human' : group.last_update, 'last_apply_human' : group.last_apply }
    return JsonResponse(data)

def database_status_all(request):
    template = loader.get_template('tools/database_status.html')
    context = RequestContext(request, { 'status' : utils.get_database_status_all() } )
    return HttpResponse(template.render(context))

def configuration_map(request):
    cmap = {}
    for cluster in Cluster.objects.all():
        if cluster.name not in cmap: cmap[cluster.name] = { 'cluster' : cluster }
        vmap = {}
        for vhost in NginxVirtualHost.objects.filter(cluster=cluster):
            if vhost.name not in vmap:  
                webs = []
                for web in Domain.objects.filter(virtual_host=vhost):
                    webs.append({ 'web' : web, 'alias' : DomainAlias.objects.filter(domain=web), 'hostredir' : HostRedir.objects.filter(domain=web) })

                urlredir = UrlRedir.objects.filter(virtual_host=vhost)
                vmap[vhost.name] = { 
                        'vhost' : vhost, 
                        'web' : webs,
                        'urlredir' : urlredir,
                        }
        cmap[cluster.name]['vhosts'] = vmap
        cmap[cluster.name]['rowspan'] = len(vmap)

    template = loader.get_template('tools/configuration_map.html')
    context = RequestContext(request, { 'clusters' : cmap } )
    return HttpResponse(template.render(context))
