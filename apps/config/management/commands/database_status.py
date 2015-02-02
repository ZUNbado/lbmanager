from django.core.management.base import BaseCommand, CommandError
from apps.config.views import get_database_status_all

from prettytable import PrettyTable

class Command(BaseCommand):
    args = ''
    help = 'Get de database status'

    def handle(self, *args, **options):
        status = get_database_status_all()
        pt = PrettyTable(['Backend', 'Version', 'Last Update', 'Last Apply', 'Need Syncro?'])
        add_current = True
        for stat in status:
            if add_current:
                pt.add_row([ 'Current', stat['current_version'], stat['current_last_update_human'], stat['current_last_apply_human'], 'Master' ])

            if stat['version'] != stat['current_version'] or stat['last_update'] != stat['current_last_update'] or stat['last_apply'] != stat['current_last_apply']: sincro = 'Yes'
            else: sincro = 'No'
            pt.add_row([ stat['backend'], stat['version'], stat['last_update_human'], stat['last_apply_human'], sincro ])

        self.stdout.write(pt.get_string())
