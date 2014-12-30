from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from .confs import GraphConf
import rrd
from datetime import datetime, timedelta
from .forms import GraphForm
import socket
from ..config.models import Group

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    end = datetime.now()
    start = end - timedelta(hours=1)
    end = end.strftime('%s')
    start = start.strftime('%s')

    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            start = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time']).strftime('%s')
            end = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['end_time']).strftime('%s')
    else:
        form = GraphForm()

    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
        'form': form,
        'graphs': confs,
        'end' : end,
        'start' : start,
        })

    return HttpResponse(template.render(context))

def index_old(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    confs = GraphConf().getgraphtypes()

    end = datetime.now()
    start = end - timedelta(hours=1)
    end = end.strftime('%s')
    start = start.strftime('%s')

    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            start = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time']).strftime('%s')
            end = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['end_time']).strftime('%s')
    else:
        form = GraphForm()
    
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
        'form': form,
        'graphs': confs,
        'end' : end,
        'start' : start,
    })

    return HttpResponse(template.render(context))


def show_image(request, graph_type, end, start):
    conf = GraphConf()
    hostname = socket.gethostname()
    config = Group.objects.get(enabled=True)
    command = conf.getconf(graph_type,'/'.join([config.graph_dir, hostname]))
    return HttpResponse(rrd.render(command, end, start, 'PNG'), 'image/png')

