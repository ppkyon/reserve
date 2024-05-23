from django.core.management.base import BaseCommand

from flow.models import UserFlowSchedule

import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        for schedule in UserFlowSchedule.objects.filter(number=0, temp_flg=True).all():
            if schedule.created_at + datetime.timedelta(minutes=15) <= datetime.datetime.now():
                schedule.delete()
        self.stdout.write(self.style.SUCCESS('reserve delete temp successfully!!'))