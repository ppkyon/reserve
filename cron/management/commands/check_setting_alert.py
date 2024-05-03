from django.core.management.base import BaseCommand

from setting.models import SettingAlert
from sign.models import AuthShop

from line.data import get_info

import uuid

class Command(BaseCommand):
    def handle(self, *args, **options):
        for shop in AuthShop.objects.filter(delete_flg=False).all():
            SettingAlert.objects.filter(shop=shop).all().delete()

            line_info = get_info(shop)
            if line_info and line_info['max_message'] and line_info['remaining_message']:
                if line_info['max_message'] == 200:
                    if line_info['remaining_message'] <= 50:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 3,
                        )
                    elif line_info['remaining_message'] <= 100:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 2,
                        )
                elif line_info['max_message'] == 5000:
                    if line_info['remaining_message'] <= 200:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 3,
                        )
                    elif line_info['remaining_message'] <= 500:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 2,
                        )
                elif line_info['max_message'] == 15000:
                    if line_info['remaining_message'] <= 500:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 3,
                        )
                    elif line_info['remaining_message'] <= 1000:
                        SettingAlert.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            text = '送信可能メッセージ数が残りわずかです。0になるとメッセージが送信されなくなります。',
                            status = 2,
                        )
        self.stdout.write(self.style.SUCCESS('check_setting_alert successfully!!'))