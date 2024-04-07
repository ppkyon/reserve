from django.http import JsonResponse

from flow.models import ShopFlowTab, ShopFlowItem, UserFlow
from richmenu.models import ShopRichMenu, ShopRichMenuItem, UserRichMenuClick
from sign.models import AuthShop, ShopLine
from user.models import LineUser

import uuid

def url(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    shop_line = ShopLine.objects.filter(shop=shop).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if UserFlow.objects.filter(user=user).exists():
        for flow_tab in ShopFlowTab.objects.filter(flow=UserFlow.objects.filter(user=user).first().flow).order_by('number').all():
            if UserFlow.objects.filter(user=user, flow_tab=flow_tab).exists():
                user_flow = UserFlow.objects.filter(user=user, flow_tab=flow_tab).first()
                if not user_flow.end_flg:
                    break

    if user_flow and user_flow.flow_tab:
        flow_item = ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab, x=1, y=1).first()
        rich_menu = ShopRichMenu.objects.filter(display_id=request.POST.get('id')).first()
        rich_menu_item = ShopRichMenuItem.objects.filter(rich_menu=rich_menu, number=request.POST.get('number')).first()

        if flow_item.analytics:
            if UserRichMenuClick.objects.filter(user=user, rich_menu_item=rich_menu_item).exists():
                rich_menu_count = UserRichMenuClick.objects.filter(user=user, rich_menu_item=rich_menu_item).first()
                rich_menu_count.count = rich_menu_count.count + 1
                rich_menu_count.save()
            else:
                UserRichMenuClick.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    rich_menu_item = rich_menu_item,
                    count = 1,
                )

        if rich_menu_item.type == 2:
            return JsonResponse( {'url': rich_menu_item.url, 'type': rich_menu_item.type}, safe=False )
        elif rich_menu_item.type == 3:
            return JsonResponse( {'url': rich_menu_item.url, 'type': rich_menu_item.type}, safe=False )
        elif rich_menu_item.type == 4:
            return JsonResponse( {'url': 'https://liff.line.me/' + str(shop_line.reserve_id), 'type': rich_menu_item.type}, safe=False )
        elif rich_menu_item.type == 5:
            return JsonResponse( {'url': 'https://liff.line.me/' + str(shop_line.history_id), 'type': rich_menu_item.type}, safe=False )
        elif rich_menu_item.type == 6:
            return JsonResponse( {'url': rich_menu_item.url, 'type': rich_menu_item.type}, safe=False )
        elif rich_menu_item.type == 7:
            return JsonResponse( {'url': rich_menu_item.url, 'type': rich_menu_item.type}, safe=False )
        return JsonResponse( {'url': rich_menu_item.url, 'type': rich_menu_item.type}, safe=False )

    return JsonResponse( {'url': ''}, safe=False )