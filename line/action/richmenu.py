
from linebot import LineBotApi
from linebot.models import MessageAction, URIAction, RichMenuSize, RichMenuArea, RichMenuBounds
from linebot.models import RichMenu as LineRichMenu

from richmenu.models import ShopRichMenu, ShopRichMenuItem, UserRichMenu
from sign.models import ShopLine

import environ
import imghdr
import os
import urllib.request as urllib_request
import uuid

env = environ.Env()
env.read_env('.env')

def create_rich_menu(user):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    user_rich_menu = UserRichMenu.objects.filter(user=user).first()
    menu_text = 'メニュー'
    if user_rich_menu:
        if user_rich_menu.rich_menu.rich_menu_id:
            rich_menu_id = user_rich_menu.rich_menu.rich_menu_id
        else:
            if user_rich_menu.rich_menu.menu_type == 1:
                menu_text = user_rich_menu.rich_menu.menu_text

            x = 0
            y = 0
            width = 0
            height = 0
            areas = []
            for rich_menu_index, rich_menu_item in enumerate(ShopRichMenuItem.objects.filter(rich_menu=user_rich_menu.rich_menu).all()):
                if user_rich_menu.rich_menu.type == 0:
                    if rich_menu_index == 3:
                        x = 0
                        y = height
                    elif rich_menu_index > 0:
                        x += width
                    width = user_rich_menu.rich_menu.image_width / 3
                    height = user_rich_menu.rich_menu.image_height / 2
                if user_rich_menu.rich_menu.type == 1:
                    if rich_menu_index == 2:
                        x = 0
                        y = height
                    elif rich_menu_index > 0:
                        x += width
                    width = user_rich_menu.rich_menu.image_width / 2
                    height = user_rich_menu.rich_menu.image_height / 2
                if user_rich_menu.rich_menu.type == 2:
                    if rich_menu_index == 1:
                        y = height
                    elif rich_menu_index > 1:
                        x += width
                    if rich_menu_index == 0:
                        width = user_rich_menu.rich_menu.image_width
                        height = user_rich_menu.rich_menu.image_height / 2
                    else:
                        width = user_rich_menu.rich_menu.image_width / 3
                        height = user_rich_menu.rich_menu.image_height / 2
                if user_rich_menu.rich_menu.type == 3:
                    if rich_menu_index == 1:
                        x = width
                    elif rich_menu_index == 2:
                        y = height
                    if rich_menu_index == 0:
                        width = user_rich_menu.rich_menu.image_width * 2 / 3
                        height = user_rich_menu.rich_menu.image_height
                    else:
                        width = user_rich_menu.rich_menu.image_width / 3
                        height = user_rich_menu.rich_menu.image_height / 2
                if user_rich_menu.rich_menu.type == 4:
                    if rich_menu_index == 1:
                        y = height
                    width = user_rich_menu.rich_menu.image_width
                    height = user_rich_menu.rich_menu.image_height / 2
                if user_rich_menu.rich_menu.type == 5:
                    if rich_menu_index == 1:
                        x = width
                    width = user_rich_menu.rich_menu.image_width / 2
                    height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 6:
                    width = user_rich_menu.rich_menu.image_width
                    height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 7:
                    if rich_menu_index > 0:
                        x += width
                    width = user_rich_menu.rich_menu.image_width / 3
                    height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 8:
                    if rich_menu_index > 0:
                        x += width
                    if rich_menu_index == 0:
                        width = user_rich_menu.rich_menu.image_width / 3
                        height = user_rich_menu.rich_menu.image_height
                    else:
                        width = user_rich_menu.rich_menu.image_width * 2 / 3
                        height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 9:
                    if rich_menu_index > 0:
                        x += width
                    if rich_menu_index == 0:
                        width = user_rich_menu.rich_menu.image_width * 2 / 3
                        height = user_rich_menu.rich_menu.image_height
                    else:
                        width = user_rich_menu.rich_menu.image_width / 3
                        height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 10:
                    if rich_menu_index > 0:
                        x += width
                    width = user_rich_menu.rich_menu.image_width / 2
                    height = user_rich_menu.rich_menu.image_height
                elif user_rich_menu.rich_menu.type == 11:
                    width = user_rich_menu.rich_menu.image_width
                    height = user_rich_menu.rich_menu.image_height

                if rich_menu_item.type == 1 or rich_menu_item.type == 2 or rich_menu_item.type == 3 or rich_menu_item.type == 4 or rich_menu_item.type == 5 or rich_menu_item.type == 6 or rich_menu_item.type == 7:
                    if shop_line.analytics_id:
                        url = 'https://liff.line.me/' + shop_line.analytics_id + '?id=' + str(rich_menu_item.rich_menu.display_id) + '&number=' + rich_menu_item.number + '&type=richmenu'
                    else:
                        url = rich_menu_item.url
                    areas.append(
                        RichMenuArea(
                            bounds=RichMenuBounds(x=x, y=y, width=width, height=height),
                            action=URIAction(label=rich_menu_item.label, uri=url),
                        )
                    )
                elif rich_menu_item.type == 8:
                    areas.append(
                        RichMenuArea(
                            bounds=RichMenuBounds(x=x, y=y, width=width, height=height),
                            action=MessageAction(label=rich_menu_item.label, text=rich_menu_item.text),
                        )
                    )

            rich_menu = LineRichMenu(
                size = RichMenuSize(width=user_rich_menu.rich_menu.image_width, height=user_rich_menu.rich_menu.image_height),
                selected = user_rich_menu.rich_menu.menu_flg,
                name = user_rich_menu.rich_menu.name,
                chat_bar_text = menu_text,
                areas=areas,
            )
            rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu)

            rich_menu = ShopRichMenu.objects.filter(id=user_rich_menu.rich_menu.id).first()
            rich_menu.rich_menu_id = rich_menu_id
            rich_menu.save()

            if env('AWS_FLG') == 'True':
                image_name = './static/' + str(uuid.uuid4()) + '.png'
                urllib_request.urlretrieve(user_rich_menu.rich_menu.image.url, image_name)
                with open(image_name, 'rb') as f:
                    line_bot_api.set_rich_menu_image(rich_menu_id, "image/" + imghdr.what(image_name), f)
            else:
                with open(user_rich_menu.rich_menu.image.url[1:], 'rb') as f:
                    line_bot_api.set_rich_menu_image(rich_menu_id, "image/" + imghdr.what(user_rich_menu.rich_menu.image.url[1:]), f)
        
            if env('AWS_FLG') == 'True':
                os.remove(image_name)

        line_bot_api.link_rich_menu_to_user(user.line_user_id, rich_menu_id)
        return rich_menu_id
    
    return None

def delete_rich_menu(user):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)
    line_bot_api.unlink_rich_menu_from_user(user.line_user_id)
    return None