from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from ..cluster.models import Member, Cluster
from ..config.models import Config
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    tempdir=Config.objects.get(name='tempdir').value+'/ldirectord'
    FilesManager.DirExists(tempdir)

    clusters = Cluster.objects.filter(enabled=True)

    tpl = loader.get_template('conf/ldirectord.cf.j2')
    ctx = RequestContext(request, { 'clusters' : clusters })
    content=tpl.render(ctx)
    FilesManager.WriteFile(tempdir+'/ldirectord.cf', content)

    # GET SSH DATA
    user=Config.objects.get(name='user').value
    password=Config.objects.get(name='password').value
    port=Config.objects.get(name='port').value


    # Copy temp data to servers
    members=Member.objects.all()
    for member in members:
        man=ConfManager(member.address,user,password,int(port))
        man.copy(tempdir+'/ldirectord.cf','/etc/ha.d/ldirectord.cf')
        man.close()


    template = loader.get_template('cluster/apply.html')
    context = RequestContext(request, { 'content': content })
    return HttpResponse(template.render(context))
    
