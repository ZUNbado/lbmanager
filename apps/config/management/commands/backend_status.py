from django.core.management.base import BaseCommand, CommandError
import apps.config.utils as config_utils

from prettytable import PrettyTable

class Command(BaseCommand):

    def handle(self, *args, **options):
        (pt, status) = config_utils.health( html = False )
        self.stdout.write(pt.get_string())
