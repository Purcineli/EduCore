from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

GROUPS = ['Students', 'Teachers', 'Parents', 'Coordinators']


class Command(BaseCommand):
    help = 'Create the default auth Groups required by EduCore (idempotent).'

    def handle(self, *args, **options):
        created_count = 0
        for name in GROUPS:
            _, created = Group.objects.get_or_create(name=name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created group: {name}'))
            else:
                self.stdout.write(f'  Already exists: {name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. {created_count} group(s) created, '
                f'{len(GROUPS) - created_count} already existed.'
            )
        )
