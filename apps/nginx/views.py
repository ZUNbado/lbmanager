from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template


from .models import NginxVirtualHost
from ..config.models import Group, Server
from ..cluster.models import Cluster
from ..web.models import Domain, DomainAlias, HostRedir, UrlRedir

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_tpl = []
    for group in Group.objects.filter(enabled=True):
        vfiles = []
        for vhost in NginxVirtualHost.objects.all():
            if vhost.cluster.filter(group=group).count() > 0:
                domains = Domain.objects.filter(enabled=True,virtual_host=vhost)
                aliases = DomainAlias.objects.filter(enabled=True,domain=domains)
                hostRedirs = HostRedir.objects.filter(enabled=True,domain=domains)
                urlRedirs = UrlRedir.objects.filter(enabled=True,virtual_host=vhost)
                tpl = loader.get_template('conf/vhost.conf.j2')
                ctx = RequestContext(request, { 'virtualhost': vhost, 'domains': domains, 'aliases': aliases, 'hostRedirs': hostRedirs, 'urlRedirs': urlRedirs })
                content=tpl.render(ctx)
                vfiles.append({ 'file': vhost.name, 'content': content })

        data_tpl.append({ 'group': group.name, 'maps': vfiles })
        
    template = loader.get_template('nginx/apply.html')
    context = RequestContext(request, {
        'data': data_tpl
    })

    return HttpResponse(template.render(context))

