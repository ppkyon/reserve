from django.core.management.base import BaseCommand

from dateutil.relativedelta import relativedelta

from common import create_code

from reception.models import ReceptionData, ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime, ManagerOffline, ManagerOnline, ManagerOfflineTime, ManagerOnlineTime
from sign.models import AuthShop, AuthUser

import calendar
import datetime
import environ
import jpholiday
import uuid

env = environ.Env()
env.read_env('.env')

class Command(BaseCommand):
    def handle(self, *args, **options):
        current = datetime.date.today().replace(day=1) + relativedelta(months=1)
        agenda = calendar.Calendar(6)
        days = agenda.monthdatescalendar(current.year, current.month)
        for shop in AuthShop.objects.filter(status__gte=2, delete_flg=False).all():
            auto = ReceptionData.objects.filter(shop=shop).first()
            if auto and auto.auto_flg:
                for shop_offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
                    for week in days:
                        for day in week:
                            if day.month == current.month:
                                date = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
                                holiday = jpholiday.is_holiday_name(datetime.date(day.year, day.month, day.day))
                                reception = ReceptionOfflinePlace.objects.filter(offline=shop_offline, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                                if not reception:
                                    if holiday:
                                        if ShopOfflineTime.objects.filter(offline=shop_offline, week=8).exists():
                                            for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=8).all():
                                                ReceptionOfflinePlace.objects.create(
                                                    id = str(uuid.uuid4()),
                                                    display_id = create_code(12, ReceptionOfflinePlace),
                                                    offline = shop_offline,
                                                    number = time.number,
                                                    reception_date = date,
                                                    reception_from = time.time_from,
                                                    reception_to = time.time_to,
                                                    reception_count = 0,
                                                    reception_flg = time.flg,
                                                )
                                        else:
                                            for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=date.isoweekday()).all():
                                                ReceptionOfflinePlace.objects.create(
                                                    id = str(uuid.uuid4()),
                                                    display_id = create_code(12, ReceptionOfflinePlace),
                                                    offline = shop_offline,
                                                    number = time.number,
                                                    reception_date = date,
                                                    reception_from = time.time_from,
                                                    reception_to = time.time_to,
                                                    reception_count = 0,
                                                    reception_flg = time.flg,
                                                )
                                    else:
                                        for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=date.isoweekday()).all():
                                            ReceptionOfflinePlace.objects.create(
                                                id = str(uuid.uuid4()),
                                                display_id = create_code(12, ReceptionOfflinePlace),
                                                offline = shop_offline,
                                                number = time.number,
                                                reception_date = date,
                                                reception_from = time.time_from,
                                                reception_to = time.time_to,
                                                reception_count = 0,
                                                reception_flg = time.flg,
                                            )
                    
                                for manager in AuthUser.objects.filter(shop=shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all():
                                    reception = ReceptionOfflineManager.objects.filter(offline=shop_offline, manager=manager, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                                    if not reception:
                                        manager_offline = ManagerOffline.objects.filter(offline=shop_offline, manager=manager).first()
                                        if manager_offline:
                                            if holiday:
                                                if ManagerOfflineTime.objects.filter(offline=manager_offline, week=8).exists():
                                                    for time in ManagerOfflineTime.objects.filter(offline=manager_offline, week=8).all():
                                                        ReceptionOfflineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOfflineManager),
                                                            offline = shop_offline,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.holiday_flg,
                                                        )
                                                else:
                                                    for time in ManagerOfflineTime.objects.filter(offline=manager_offline, week=date.isoweekday()).all():
                                                        ReceptionOfflineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOfflineManager),
                                                            offline = shop_offline,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.holiday_flg,
                                                        )
                                            else:
                                                for time in ManagerOfflineTime.objects.filter(offline=manager_offline, week=date.isoweekday()).all():
                                                    ReceptionOfflineManager.objects.create(
                                                        id = str(uuid.uuid4()),
                                                        display_id = create_code(12, ReceptionOfflineManager),
                                                        offline = shop_offline,
                                                        number = time.number,
                                                        manager = manager,
                                                        reception_date = date,
                                                        reception_from = time.time_from,
                                                        reception_to = time.time_to,
                                                        reception_flg = not time.holiday_flg,
                                                    )
                                        else:
                                            if holiday:
                                                if ShopOfflineTime.objects.filter(offline=shop_offline, week=8).exists():
                                                    for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=8).all():
                                                        ReceptionOfflineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOfflineManager),
                                                            offline = shop_offline,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.flg,
                                                        )
                                                else:
                                                    for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=date.isoweekday()).all():
                                                        ReceptionOfflineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOfflineManager),
                                                            offline = shop_offline,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.flg,
                                                        )
                                            else:
                                                for time in ShopOfflineTime.objects.filter(offline=shop_offline, week=date.isoweekday()).all():
                                                    ReceptionOfflineManager.objects.create(
                                                        id = str(uuid.uuid4()),
                                                        display_id = create_code(12, ReceptionOfflineManager),
                                                        offline = shop_offline,
                                                        number = time.number,
                                                        manager = manager,
                                                        reception_date = date,
                                                        reception_from = time.time_from,
                                                        reception_to = time.time_to,
                                                        reception_flg = not time.flg,
                                                    )
                
                for shop_online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
                    for week in days:
                        for day in week:
                            if day.month == current.month:
                                date = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
                                holiday = jpholiday.is_holiday_name(datetime.date(day.year, day.month, day.day))
                                reception = ReceptionOnlinePlace.objects.filter(online=shop_online, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                                if not reception:
                                    if holiday:
                                        if ShopOnlineTime.objects.filter(online=shop_online, week=8).exists():
                                            for time in ShopOnlineTime.objects.filter(online=shop_online, week=8).all():
                                                ReceptionOnlinePlace.objects.create(
                                                    id = str(uuid.uuid4()),
                                                    display_id = create_code(12, ReceptionOnlinePlace),
                                                    online = shop_online,
                                                    number = time.number,
                                                    reception_date = date,
                                                    reception_from = time.time_from,
                                                    reception_to = time.time_to,
                                                    reception_count = 0,
                                                    reception_flg = time.flg,
                                                )
                                        else:
                                            for time in ShopOnlineTime.objects.filter(online=shop_online, week=date.isoweekday()).all():
                                                ReceptionOnlinePlace.objects.create(
                                                    id = str(uuid.uuid4()),
                                                    display_id = create_code(12, ReceptionOnlinePlace),
                                                    online = shop_online,
                                                    number = time.number,
                                                    reception_date = date,
                                                    reception_from = time.time_from,
                                                    reception_to = time.time_to,
                                                    reception_count = 0,
                                                    reception_flg = time.flg,
                                                )
                                    else:
                                        for time in ShopOnlineTime.objects.filter(online=shop_online, week=date.isoweekday()).all():
                                            ReceptionOnlinePlace.objects.create(
                                                id = str(uuid.uuid4()),
                                                display_id = create_code(12, ReceptionOnlinePlace),
                                                online = shop_online,
                                                number = time.number,
                                                reception_date = date,
                                                reception_from = time.time_from,
                                                reception_to = time.time_to,
                                                reception_count = 0,
                                                reception_flg = time.flg,
                                            )
                    
                                for manager in AuthUser.objects.filter(shop=shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all():
                                    reception = ReceptionOnlineManager.objects.filter(online=shop_online, manager=manager, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                                    if not reception:
                                        manager_online = ManagerOnline.objects.filter(online=shop_online, manager=manager).first()
                                        if manager_online:
                                            if holiday:
                                                if ManagerOnlineTime.objects.filter(online=manager_online, week=8).exists():
                                                    for time in ManagerOnlineTime.objects.filter(online=manager_online, week=8).all():
                                                        ReceptionOnlineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOnlineManager),
                                                            online = shop_online,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.holiday_flg,
                                                        )
                                                else:
                                                    for time in ManagerOnlineTime.objects.filter(online=manager_online, week=date.isoweekday()).all():
                                                        ReceptionOnlineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOnlineManager),
                                                            online = shop_online,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.holiday_flg,
                                                        )
                                            else:
                                                for time in ManagerOnlineTime.objects.filter(online=manager_online, week=date.isoweekday()).all():
                                                    ReceptionOnlineManager.objects.create(
                                                        id = str(uuid.uuid4()),
                                                        display_id = create_code(12, ReceptionOnlineManager),
                                                        online = shop_online,
                                                        number = time.number,
                                                        manager = manager,
                                                        reception_date = date,
                                                        reception_from = time.time_from,
                                                        reception_to = time.time_to,
                                                        reception_flg = not time.holiday_flg,
                                                    )
                                        else:
                                            if holiday:
                                                if ShopOnlineTime.objects.filter(online=shop_online, week=8).exists():
                                                    for time in ShopOnlineTime.objects.filter(online=shop_online, week=8).all():
                                                        ReceptionOnlineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOnlineManager),
                                                            online = shop_online,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.flg,
                                                        )
                                                else:
                                                    for time in ShopOnlineTime.objects.filter(online=shop_online, week=date.isoweekday()).all():
                                                        ReceptionOnlineManager.objects.create(
                                                            id = str(uuid.uuid4()),
                                                            display_id = create_code(12, ReceptionOnlineManager),
                                                            online = shop_online,
                                                            number = time.number,
                                                            manager = manager,
                                                            reception_date = date,
                                                            reception_from = time.time_from,
                                                            reception_to = time.time_to,
                                                            reception_flg = not time.flg,
                                                        )
                                            else:
                                                for time in ShopOnlineTime.objects.filter(online=shop_online, week=date.isoweekday()).all():
                                                    ReceptionOnlineManager.objects.create(
                                                        id = str(uuid.uuid4()),
                                                        display_id = create_code(12, ReceptionOnlineManager),
                                                        online = shop_online,
                                                        number = time.number,
                                                        manager = manager,
                                                        reception_date = date,
                                                        reception_from = time.time_from,
                                                        reception_to = time.time_to,
                                                        reception_flg = not time.flg,
                                                    )

        self.stdout.write(self.style.SUCCESS('reception_auto_update successfully!!'))