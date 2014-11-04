from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from ..cluster.models import Member, Cluster
from ..config.models import Config, Group, Server
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    final_content = []
    for group in Group.objects.filter(enabled=True):
        tempdir=temp_dir=Config.objects.get(group=group).temp_dir+'/'+str(group.id)
        FilesManager.DirExists(tempdir)

        clusters = Cluster.objects.filter(enabled=True,group=group)

        tpl = loader.get_template('conf/ldirectord.cf.j2')
        ctx = RequestContext(request, { 'clusters' : clusters })
        content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/ldirectord.cf', content)

        final_members = {}
        servers=Config.objects.get(group=group).cluster_servers
        for server in servers.all(): 
            final_members[server.name]=server
        if len(final_members) == 0:
            # Get all servers from a group
            clusters=Cluster.objects.filter(group=group)
            for cluster in clusters:
                members=Member.objects.filter(cluster=cluster)
                for member in members:
                    if member.server.name not in final_members:
                        final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            if Config.objects.get(group=group).enable_transfer is  True:
                man=ConfManager(
                    member.address,
                    member.ssh_user,
                    member.ssh_password,
                    member.ssh_port
                )
                man.copy(tempdir+'/ldirectord.cf','/etc/ha.d/ldirectord.cf')
                man.close()
        final_content.append({ 'group': group.name, 'content': content })

    template = loader.get_template('cluster/apply.html')
    context = RequestContext(request, { 'content': final_content })
    return HttpResponse(template.render(context))
    
