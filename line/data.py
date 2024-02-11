from sign.models import ShopLine

import datetime
import math
import requests

def get_info(shop):
    shop_line = ShopLine.objects.filter(shop=shop).first()
    line_info = {}
    if shop and shop_line and shop_line.channel_access_token:
        responce = requests.get("https://api.line.me/v2/bot/message/quota", 
            headers = {
                'Authorization': 'Bearer ' + shop_line.channel_access_token,
                'Content-Type': "application/json"
            },
        ).json()
        line_info['max_message'] = responce['value']

        responce = requests.get("https://api.line.me/v2/bot/message/quota/consumption", 
            headers = {
                'Authorization': 'Bearer ' + shop_line.channel_access_token,
                'Content-Type': "application/json"
            },
        ).json()
        line_info['count_message'] = responce['totalUsage']
        
        line_info['remaining_message'] = line_info['max_message'] - line_info['count_message']
        line_info['percent_message'] = 100 - math.floor(line_info['count_message'] / line_info['max_message'] * 100)
        
        qrcode = None
        if shop_line.bot_id:
            qrcode = 'https://qr-official.line.me/sid/L/' + shop_line.bot_id.replace('@', '') + '.png'
        line_info['qrcode'] = qrcode

        line_info['now'] = datetime.datetime.now()
    return line_info