from django.core.management.base import BaseCommand

from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace
from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting, ReserveCalendarDate
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthShop

import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        for shop in AuthShop.objects.filter(status__gte=2, delete_flg=False).all():
            for offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
                for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
                    for all_date_item in ReceptionOfflinePlace.objects.filter(offline=offline, number=1).order_by('reception_date').all():
                        date = all_date_item.reception_date
                        if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) < datetime.datetime.now():
                            ReserveCalendarDate.objects.filter(date=date, offline=offline_setting).all().delete()
            for online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
                for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
                    for all_date_item in ReceptionOnlinePlace.objects.filter(online=online, number=1).order_by('reception_date').all():
                        date = all_date_item.reception_date
                        if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) < datetime.datetime.now():
                            ReserveCalendarDate.objects.filter(date=date, online=online_setting).all().delete()
        self.stdout.write(self.style.SUCCESS('reserve calendar create successfully!!'))