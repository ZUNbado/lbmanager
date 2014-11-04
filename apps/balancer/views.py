from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import Director, Backend
from ..cluster.models import Member, Cluster
from ..config.models import Config, Group
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    content = []
    for group in groups:
        tempdir=temp_dir=Config.objects.get(group=group).temp_dir+'/'+str(group.id)
        varnish_dir=temp_dir=Config.objects.get(group=group).varnish_dir
        FilesManager.DirExists(tempdir)

        directors = Director.objects.filter(enabled=True,group=group)

        tpl = loader.get_template('conf/backends.vcl.j2')
        ctx = RequestContext(request, { 'directors' : directors })
        tpl_content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/backend.vcl', tpl_content)
        content.append({ 'group': group.name, 'content': tpl_content })

        # Get all servers from a group
        clusters=Cluster.objects.filter(group=group)
        final_members = {}
        for cluster in clusters:
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members:
                    final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            man=ConfManager(member.server.address, member.server.ssh_user, member.server.ssh_password, member.server.ssh_port )
            if Config.objects.get(group=group).enable_transfer is  True:
                man.copy(tempdir+'/backend.vcl',varnish_dir+'/default.vcl')
            if Config.objects.get(group=group).enable_reload is True:
                man.command('service varnish start')
            man.close()
                

    template = loader.get_template('balancer/apply.html')
    context = RequestContext(request, { 'content': content })
    return HttpResponse(template.render(context))
