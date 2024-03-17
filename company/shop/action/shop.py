from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import get_template

from fixture.models import Prefecture
from sign.models import AuthShop, AuthUser, ShopProfile, ShopLine, ManagerProfile, AuthLogin
from tag.models import CompanyTag, ShopHashTag

from company.shop.action.list import get_list

from common import create_code, create_password, get_model_field
from table.action import action_search

import environ
import phonenumbers
import uuid

env = environ.Env()
env.read_env('.env')

def add(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    auth_shop = AuthShop.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, AuthShop),
        company = auth_login.company,
        status = 1,
        delete_flg = False,
    )

    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
    else:
        site_name = env('SITE_NAME')
    subject = '【アトエル】店舗の新規アカウント登録メール'
    template = get_template('company/shop/email/add.txt')
    site = get_current_site(request)
    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': site.domain,
        'site_name': site_name,
        'id': auth_shop.display_id,
    }
    send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [request.POST.get("email")])

    return JsonResponse( {}, safe=False )

def save(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).first()
    shop_profile = ShopProfile.objects.filter(shop=shop).first()
    shop_profile.head_family_name = request.POST.get('head_family_name')
    shop_profile.head_first_name = request.POST.get('head_first_name')
    shop_profile.head_family_name_kana = request.POST.get('head_family_name_kana')
    shop_profile.head_first_name_kana = request.POST.get('head_first_name_kana')
    shop_profile.shop_name = request.POST.get('shop_name')
    shop_profile.shop_postcode = request.POST.get('shop_postcode').replace('-', '')
    shop_profile.shop_prefecture = Prefecture.objects.filter(value=request.POST.get('shop_prefecture')).first()
    shop_profile.shop_address = request.POST.get('shop_address')
    shop_profile.shop_phone_number = request.POST.get('shop_phone_number').replace('-', '')
    shop_profile.memo = request.POST.get('memo')
    shop_profile.save()

    ShopHashTag.objects.filter(shop=shop).all().delete()
    if request.POST.get('tag[]'):
        for tag_index, tag_item in enumerate( request.POST.get('tag[]').split(',') ):
            ShopHashTag.objects.create(
                id = str(uuid.uuid4()),
                shop = shop,
                number = (tag_index+1),
                tag = CompanyTag.objects.filter(display_id=tag_item).first()
            )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).first()
    shop.delete_flg = True
    shop.save()
    return JsonResponse( {}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, None, auth_login.company)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def start(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).first()
    shop_profile = ShopProfile.objects.filter(shop=shop).first()
    if not AuthUser.objects.filter(email=shop_profile.manager_email).exists():
        password = create_password()
        manager = AuthUser.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, AuthUser),
            company = None,
            shop = shop,
            email = shop_profile.manager_email,
            password = make_password(password),
            authority = 3,
            status = 1,
            author = None,
        )

        ManagerProfile.objects.create(
            id = str(uuid.uuid4()),
            manager = manager,
            family_name = shop_profile.manager_family_name,
            first_name = shop_profile.manager_first_name,
            family_name_kana = shop_profile.manager_family_name_kana,
            first_name_kana = shop_profile.manager_first_name_kana,
            image = shop_profile.manager_image,
            phone_number = shop_profile.manager_phone_number,
            department = shop_profile.manager_department,
        )

        if env('ENCODING') == 'True':
            site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
        else:
            site_name = env('SITE_NAME')
        subject = '【アトエル】IDとパスワードの送付'
        template = get_template('setting/email/add_manager.txt')
        site = get_current_site(request)
        context = {
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': site.domain,
            'site_name': site_name,
            'user': manager,
            'password': password,
        }
        send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [manager.email])
    
    shop.status = 3
    shop.save()

    return JsonResponse( {}, safe=False )



def save_line(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).first()
    if ShopLine.objects.filter(shop=shop).exists():
        shop_line = ShopLine.objects.filter(shop=shop).first()
        shop_line.channel_id = request.POST.get('channel_id')
        shop_line.channel_secret = request.POST.get('channel_secret')
        shop_line.channel_access_token = request.POST.get('channel_access_token')
        shop_line.bot_id = request.POST.get('bot_id')
        shop_line.liff_id = request.POST.get('liff_id')
        shop_line.analytics_id = request.POST.get('analytics_id')
        shop_line.qrcode_id = request.POST.get('qrcode_id')
        shop_line.reserve_id = request.POST.get('reserve_id')
        shop_line.history_id = request.POST.get('history_id')
        shop_line.follow_url = request.POST.get('follow_url')
        shop_line.save()
    else:
        ShopLine.objects.create(
            id = str(uuid.uuid4()),
            shop = shop,
            channel_id = request.POST.get('channel_id'),
            channel_secret = request.POST.get('channel_secret'),
            channel_access_token = request.POST.get('channel_access_token'),
            bot_id = request.POST.get('bot_id'),
            liff_id = request.POST.get('liff_id'),
            analytics_id = request.POST.get('analytics_id'),
            qrcode_id = request.POST.get('qrcode_id'),
            reserve_id = request.POST.get('reserve_id'),
            history_id = request.POST.get('history_id'),
            follow_url = request.POST.get('follow_url'),
        )
    return JsonResponse( {}, safe=False )



def get_profile(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(AuthShop)).first()
    shop['profile'] = ShopProfile.objects.filter(shop__id=shop['id']).values(*get_model_field(ShopProfile)).first()
    shop['prefecture'] = Prefecture.objects.filter(id=shop['profile']['shop_prefecture']).values(*get_model_field(Prefecture)).first()
    shop['phone_number'] = phonenumbers.format_number(phonenumbers.parse(shop['profile']['shop_phone_number'], 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
    shop['display_date'] = shop['created_at'].strftime('%Y年%m月%d日 %H:%M')

    tag_list = list()
    for shop_tag_item in ShopHashTag.objects.filter(shop__id=shop['id']).order_by('number').all():
        tag_list.append( CompanyTag.objects.filter(id=shop_tag_item.tag.id).values(*get_model_field(CompanyTag)).first())
    shop['tag'] = tag_list
    return JsonResponse( {'shop': shop}, safe=False )