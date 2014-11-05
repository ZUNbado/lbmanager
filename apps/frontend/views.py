from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template

from .models import DomainAlias, Domain, HostRedir, UrlRedir, VirtualHost
from ..cluster.models import Member, Cluster
from ..config.models import Group, Config, Server
from ..balancer.models import Director
from libs.confmanager import ConfManager, FilesManager


def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    data_tpl = []
    status = []
    for group in groups:

        files_copy=[]
        maps = []
        nginx_maps_dir=Config.objects.get(group=group).nginx_maps_dir
        nginx_conf_dir=Config.objects.get(group=group).nginx_conf_dir
        nginx_sites_dir=Config.objects.get(group=group).nginx_sites_dir
        temp_dir=Config.objects.get(group=group).temp_dir+'/'+str(group.id)

        temp_dir_maps=temp_dir+'/nginx/maps/'
        FilesManager.DirExists(temp_dir_maps)
        
        # Obtain data
        directors = Director.objects.filter(group=group)
        domains = Domain.objects.filter(enabled=True,director=directors)
        domainalias = DomainAlias.objects.filter(enabled=True,domain=domains)
        alias = []
        for domain in domains: alias.append({ 'alias': domain.name, 'name': domain.name })
        for domalias in domainalias: alias.append({ 'alias': domalias.name, 'name': domalias.domain.name })
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
            tpl = loader.get_template('conf/'+fl['name']+'.j2')
            ctx = RequestContext(request, { 'data' : fl['data'] })
            content=tpl.render(ctx)
            FilesManager.WriteFile(temp_dir_maps+'/'+fl['name'], content)
            maps.append({'file': fl['desc'], 'content': content})
            files_copy.append({ 'src': temp_dir_maps+'/'+fl['name'], 'dst': nginx_maps_dir+'/'+fl['name'] })
    
        temp_dir_conf=temp_dir+'/nginx/conf.d'
        FilesManager.DirExists(temp_dir_conf)
        files = [ 'backend.conf', 'cache.conf', 'normalize.conf', 'redir.conf', 'redir_url.conf']
        for fl in files:
            tpl = loader.get_template('conf/'+fl+'.j2')
            ctx = RequestContext(request, { 'nginx_map_dir': nginx_maps_dir})
            content=tpl.render(ctx)
            FilesManager.WriteFile(temp_dir_conf+'/'+fl, content)
            files_copy.append({ 'src': temp_dir_conf+'/'+fl, 'dst': nginx_conf_dir+'/'+fl })

        # Get all servers from a group (for virtualhosts and members to copy fileS)
        clusters=Cluster.objects.filter(group=group)

        # Generate vhosts
        temp_dir_sites=temp_dir+'/nginx/sites'
        FilesManager.DirExists(temp_dir_sites)
        virtualhosts = VirtualHost.objects.filter(clusters=clusters).distinct()
        for virtualhost in virtualhosts:
            tpl = jinja_template(virtualhost.virtualhosttype.template)
            content = tpl.render({ 'virtualhost': virtualhost, 'clusters': virtualhost.clusters })
            FilesManager.WriteFile(temp_dir_sites+'/'+virtualhost.name, content)
            files_copy.append({ 'src': temp_dir_sites+'/'+virtualhost.name, 'dst': nginx_sites_dir+'/'+virtualhost.name+'.conf' })
            maps.append({ 'file': virtualhost.name, 'content': content })

        # Get members to copy files    
        final_members = {}
        for cluster in clusters:
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members: 
                    final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            config=Config.objects.get(group=group)
            msg = ''
            man=ConfManager( member.server.address, member.server.ssh_user, member.server.ssh_password, member.server.ssh_port )
            if man.connected:
                if config.enable_transfer is  True:
                    man.command('mkdir -p '+nginx_maps_dir)
                    man.command('mkdir -p '+nginx_conf_dir)
                    for fl in files_copy:
                        man.copy(fl['src'],fl['dst'])
                    msg = "Files transferred"
                else:
                    msg = "Transfer files disabled"

                if config.enable_reload is  True:
                    man.command('service nginx reload')
                    msg = msg + "Service restarted"
                else:
                    msg = msg + "Reload services disabled"

                man.close()
            else:
                msg = "Error connecting host: %s" % man.error_msg
            status.append({ 'name': member.name, 'msg': msg })

        data_tpl.append({ 'group': group.name, 'maps': maps })
    
    template = loader.get_template('frontend/apply.html')
    context = RequestContext(request, {
        'data': data_tpl,
        'status': status,
    })

    return HttpResponse(template.render(context))
