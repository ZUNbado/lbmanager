from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from ..cluster.models import Member, Cluster
from ..config.models import Group, Server
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    final_content = []
    status = []
    for group in Group.objects.filter(enabled=True):
        tempdir=group.temp_dir+'/'+str(group.id)
        FilesManager.DirExists(tempdir)

        clusters = Cluster.objects.filter(enabled=True,group=group)

        tpl = loader.get_template('conf/ldirectord.cf.j2')
        ctx = RequestContext(request, { 'clusters' : clusters })
        content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/ldirectord.cf', content)

        final_members = {}
        servers=group.cluster_servers
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
            if group.enable_transfer is True or group.enable_reload is True:
                man=ConfManager(member.address, member.ssh_user, member.ssh_password, member.ssh_port )
                msg = ''
                if man.connected:
                    if group.enable_transfer is True:
                        man.copy(tempdir+'/ldirectord.cf','/etc/ha.d/ldirectord.cf')
                        msg = "Files transferred"
                    else:
                        msg = "Transfer files disabled"

                    if group.enable_reload is True:
                        man.command('service ldirectord restart')
                        msg = msg + "Service restarted"
                    else:
                        msg = msg + "Reload services disabled"
    
                    man.close()
                else:
                    msg = "Error connecting host: %s" % man.error_msg
            else:
                msg = "Configuration disabled"
            status.append({ 'name': member.name, 'msg': msg })
        final_content.append({ 'group': group.name, 'content': content })

    template = loader.get_template('cluster/apply.html')
    context = RequestContext(request, { 'content': final_content, 'status': status })
    return HttpResponse(template.render(context))
