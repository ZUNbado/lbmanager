from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import DomainAlias
from apps.cluster.models import Member
from apps.config.models import Config
from libs.ssh import Connect


def apply(request):
	if not request.user.is_authenticated():
		return redirect('/admin/login/?next=%s' % request.path)

	alias = DomainAlias.objects.all()
	template = loader.get_template('frontend/apply.html')
	context = RequestContext(request, {
		'alias': alias,
	})


	user=Config.objects.get(name='user').value
	password=Config.objects.get(name='password').value
	port=Config.objects.get(name='port').value

	members=Member.objects.all()
	for member in members:
		lala=Connect(member.address,user,password,int(port))
		lala.copy('/tmp/src','/tmp/dst')
		lala.command('touch /tmp/touch')
	return HttpResponse(template.render(context))
