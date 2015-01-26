from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
import rrd
from datetime import datetime, timedelta
from .forms import GraphForm
from ..config.models import Group, Server
from .models import Graph, GraphTypes

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    servers = {}
    for server in Server.objects.filter(enabled=True):
        for graph in Graph.objects.filter(server=server).order_by('graph'):
            if server.name not in servers: servers[server.name] = { 'server': server, 'graphs': [] }
            if graph not in servers[server.name]['graphs']: servers[server.name]['graphs'].append(graph)

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
        'servers': servers,
        'end' : end,
        'start' : start,
        'config' : Group.objects.get(enabled=True)
        })

    return HttpResponse(template.render(context))


def show_image(request, graph, end, start):
    command = Graph.objects.get(pk=graph).get_conf()
    return HttpResponse(rrd.render(command, end, start, 'PNG'), 'image/png')

