from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import Director, Backend
from ..cluster.models import Member
from libs.confmanager import ConfManager, FilesManager

def apply(request):
	if not request.user.is_authenticated():
		return redirect('/admin/login/?next=%s' % request.path)

	#tempdir=Config.objects.get(name='tempdir').value+'/varnish'
	FilesManager.DirExists(tempdir)

	directors = Director.objects.filter(enabled=True)
	backends = Backend.objects.filter(enabled=True)

	tpl = loader.get_template('conf/backends.vcl')
	ctx = RequestContext(request, { 'directors' : directors, 'backends': backends })
	content=tpl.render(ctx)
	FilesManager.WriteFile(tempdir+'/backend.vcl', content)

	template = loader.get_template('balancer/apply.html')
	context = RequestContext(request, { 'content': content })
	return HttpResponse(template.render(context))
