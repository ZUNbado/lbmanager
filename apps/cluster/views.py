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
#    virtual = {}
#    for cluster in clusters:
#        if not cluster.name in virtual: virtual[cluster.name]={ 'cluster': cluster, 'members': [] }
#    	members = Member.objects.filter(enabled=True, )

	tpl = loader.get_template('conf/ldirectord.cf.j2')
#	ctx = RequestContext(request, { 'directors' : directors, 'backends': backends })
	ctx = RequestContext(request, { 'clusters' : clusters })
	content=tpl.render(ctx)
	FilesManager.WriteFile(tempdir+'/ldirectord.cf', content)

	template = loader.get_template('cluster/apply.html')
	context = RequestContext(request, { 'content': content })
	return HttpResponse(template.render(context))
	
