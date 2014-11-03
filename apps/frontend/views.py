from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import DomainAlias, Domain, HostRedir, UrlRedir
from ..cluster.models import Member, Cluster
from ..config.models import Group, Config, Server
from ..balancer.models import Director
from libs.confmanager import ConfManager, FilesManager


def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    data_tpl = []
    for group in groups:

        files_copy=[]
        maps = []
        nginx_maps_dir=Config.objects.get(group=group).nginx_maps_dir
        nginx_conf_dir=Config.objects.get(group=group).nginx_conf_dir
        temp_dir=Config.objects.get(group=group).temp_dir+'/'+str(group.id)

        temp_dir_maps=temp_dir+'/nginx/maps/'
        FilesManager.DirExists(temp_dir_maps)
        
        # Obtain data
        directors = Director.objects.filter(group=group)
        domains = Domain.objects.filter(enabled=True,director=directors)
        alias = DomainAlias.objects.filter(enabled=True,domain=domains)
        hostredir = HostRedir.objects.filter(enabled=True,domain=domains)
        urlredir = UrlRedir.objects.filter(enabled=True)

        files = [ 
            { 'name': 'backend.map', 'data': domains, 'desc' : 'Domains'},
            { 'name': 'cache.map', 'data': domains, 'desc': 'Enabled Cache' },
            { 'name': 'normalize.map', 'data': alias, 'desc': 'Alias' } ,
            { 'name': 'redir.map', 'data': hostredir, 'desc': 'Host Redir' },
            { 'name': 'redir_url.map', 'data': urlredir, 'desc': 'URL Redir' },
        ]
        for fl in files:
            tpl = loader.get_template('conf/'+fl['name'])
            ctx = RequestContext(request, { 'data' : fl['data'] })
            content=tpl.render(ctx)
            FilesManager.WriteFile(temp_dir_maps+'/'+fl['name'], content)
            maps.append({'file': fl['desc'], 'content': content})
            files_copy.append({ 'src': temp_dir_maps+'/'+fl['name'], 'dst': nginx_maps_dir+'/'+fl['name'] })
    
        temp_dir_conf=temp_dir+'/nginx/conf.d'
        FilesManager.DirExists(temp_dir_conf)
        files = [ 'backend.conf', 'cache.conf', 'normalize.conf', 'redir.conf', 'redir_url.conf']
        for fl in files:
            tpl = loader.get_template('conf/'+fl)
            ctx = RequestContext(request, { 'nginx_map_dir': nginx_maps_dir})
            content=tpl.render(ctx)
            FilesManager.WriteFile(temp_dir_conf+'/'+fl, content)
            files_copy.append({ 'src': temp_dir_conf+'/'+fl, 'dst': nginx_conf_dir+'/'+fl })
    
        # Get all servers from a group
        clusters=Cluster.objects.filter(group=group)
        final_members = {}
        for cluster in clusters:
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members: 
                    final_members[member.server.name]=member.server

        for member in final_members:
            if Config.objects.get(group=group).enable_transfer is  True:
                man=ConfManager(
                    member.server.address,
                    member.server.ssh_user,
                    member.server.ssh_password,
                    member.server.ssh_port
                )
                man.command('mkdir -p '+nginx_maps_dir)
                man.command('mkdir -p '+nginx_conf_dir)
                for fl in files_copy:
                    man.copy(fl['src'],fl['dst'])
                man.close()
        data_tpl.append({ 'group': group.name, 'maps': maps })
    
    template = loader.get_template('frontend/apply.html')
    context = RequestContext(request, {
        'data': data_tpl,
    })

    return HttpResponse(template.render(context))
