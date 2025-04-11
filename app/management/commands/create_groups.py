from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create User and Admin groups'

    def handle(self, *args, **kwargs):
        # Create user group
        user_group, created = Group.objects.get_or_create(name='User')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created User group'))

        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Admin group'))
