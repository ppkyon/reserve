from django.core.management.base import BaseCommand

from flow.models import UserFlow, UserFlowSchedule
from user.models import LineUser, UserAlert

import datetime
import uuid

class Command(BaseCommand):
    def handle(self, *args, **options):
        for user_item in LineUser.objects.filter(delete_flg=False).all():
            UserAlert.objects.filter(user=user_item).all().delete()
            for user_flow in UserFlow.objects.filter(user=user_item, end_flg=False).order_by('number').all():
                for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow).all():
                    if user_flow_schedule.join == 0:
                        if user_flow_schedule.date and user_flow_schedule.time:
                            interview_date = user_flow_schedule.date.replace(hour=user_flow_schedule.time.hour, minute=user_flow_schedule.time.minute, second=0, microsecond=0)

                            if interview_date:
                                if interview_date <= datetime.datetime.now():
                                    UserAlert.objects.create(
                                        id = str(uuid.uuid4()),
                                        user = user_item,
                                        number = user_flow.number,
                                        text = '予約日時を過ぎた日程があります。',
                                        status = 3,
                                    )
        self.stdout.write(self.style.SUCCESS('check_join_alert successfully!!'))