from .models import Group, Server
from ..cluster.models import Member
from libs.confmanager import ConfManager, FilesManager
import os, shutil, re
from prettytable import PrettyTable
import requests
from django.core.urlresolvers import reverse

def sync():
    root = os.path.abspath(os.path.dirname(__name__))

    config = Group.objects.get(enabled=True)

    dbfile = '/db.sqlite3'

    if not os.path.exists(config.temp_dir): os.makedirs(config.temp_dir)
    shutil.copy2(root+dbfile, config.temp_dir)

    # cal canviar aixo perque agafi els membres d'un cluster enlloc de TOTS els servers (als backends no s'ha de copiar)
    status = []
    if config.enable_transfer is True:
        for server in Server.objects.filter(role_frontend=True):
            if Member.objects.filter(server=server):
                man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
                if man.connected:
                    man.copy(config.temp_dir+dbfile, config.app_path+dbfile)
                    msg = "Database synced"
                else:
                    msg = "Error connecting host: %s" % man.error_msg

                status.append({ 'name' : server.name, 'msg': msg })
    else:
        status.append({ 'name': '', 'msg' : 'Transfer is disabled' })

    return status

def get_database_status_all():
    group = Group.objects.get(pk=1)

    status = []
    for server in Server.objects.filter(role_cluster=True):
        stat = requests.get('http://%s:8000/admin/database/custom/database_status' % server.address ).json()
        stat['backend'] = server.name
        stat['current_version'] = group.version
        stat['current_last_update'] = group.last_update.strftime('%s') if group.last_update else None
        stat['current_last_apply'] = group.last_apply.strftime('%s') if group.last_apply else None
        stat['current_last_update_human'] = group.last_update
        stat['current_last_apply_human'] = group.last_apply

        status.append(stat)

    return status


def backend_set_state(backend_name, state):
    for server in Server.objects.filter(role_frontend=True):
        if Member.objects.filter(server=server):
            man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
            if man.connected:
                man.command('varnishadm backend.set_health %s %s' % (backend_name, state))


def health( html = True):
    backend_status = {}
    backends_name = []
    status = []
    for server in Server.objects.filter(role_frontend=True):
        if Member.objects.filter(server=server):
            man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
            if man.connected:
                if not server.name in backend_status: backend_status[server.name] = {}
                man.command('varnishadm backend.list')
                regex = '([A-Za-z0-9_]+)\(\d+\.\d+\.\d+\.\d+,,\d+\)\s+\d+\s+(\w+)\s+(\w+)\s+([a-zA-Z0-9\(\) |0-9\/]+)'
                for (bck_name, bck_status, bck_health, bck_probe) in  re.findall(regex, man.stdout.read(), re.S | re.M):
                    if not bck_name in backends_name: backends_name.append(bck_name)
                    if not bck_name in backend_status[server.name]: backend_status[server.name][bck_name] = {}
                    backend_status[server.name][bck_name] = { 'name' : bck_name, 'status' : bck_status, 'health' : bck_health, 'probe' : bck_probe }

                msg = "Data received"
            else:
                msg = "Error connecting host: %s" % man.error_msg

            status.append({ 'name' : server.name, 'msg': msg })

    headers = [ 'Frontals\Backends' ]
    rows = {}
    links = {}
    for backend in backends_name:
        if not '##%s##' % backend in links:
            enable = reverse('apps.config.views.backend_enable', args = { backend } )
            disable = reverse('apps.config.views.backend_disable', args = { backend } )
            link = '%s <a href="%s"><img src="/static/config/images/start.png"></a>/<a href="%s"><img src="/static/config/images/stop.png"></a>' % (backend, enable, disable)
            links['##%s##' % backend] = link

        headers.append('##%s##' % backend) 
        for front in backend_status:
            if not front in rows: rows[front] = []
            rows[front].append(backend_status[front][backend]['status'])

    grid = PrettyTable( headers )
    for front, row in rows.items():
        grid.add_row( [ front ] + row )
    
    if html:
        grid.attributes = { 'width' : '1200' }
        grid = grid.get_html_string() 
        for backend, link in links.items():
            grid = grid.replace(backend, link)

    return (grid, status)
