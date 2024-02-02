from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.shortcuts import render

from django.views.generic import View

from fixture.models import Country, Prefecture, WorkParent, WorkChild
from sign.models import AuthShop, AuthCompany, ShopProfile, CompanyProfile
from tag.models import HeadTagGenre, HeadTag, CompanyTagGenre, CompanyTag, CompanyHashTag, ShopHashTag

from common import create_code

import base64
import environ
import phonenumbers
import uuid

env = environ.Env()
env.read_env('.env')

class CompanyView(View):
    template_name = 'account/company/index.html'
    title = '企業アカウントの作成'

    def get(self, request, **kwargs):
        company = None
        if request.GET.get("id"):
            company = AuthCompany.objects.filter(display_id=request.GET.get("id"), status=1).first()

        data = {
            'title': self.title,
            'company': company,
            'prefecture_list': Prefecture.objects.order_by('number').all(),
            'work_parent_list': WorkParent.objects.order_by('number').all(),
        }
        return render(self.request, self.template_name, data)

    def post(self, request, **kwargs):
        company = None
        if request.POST.get("id"):
            company = AuthCompany.objects.filter(display_id=request.POST.get("id"), status=1).first()
        data = {
            'title': self.title,
            'company': company,
            'input': get_company_data(request),
            'prefecture_list': Prefecture.objects.order_by('number').all(),
            'work_parent_list': WorkParent.objects.order_by('number').all(),
        }
        return render(self.request, self.template_name, data)

class CompanyCheckView(View):
    template_name = 'account/company/check.html'
    title = '企業アカウントの作成'

    def post(self, request, **kwargs):
        data = {
            'title': self.title,
            'input': get_company_data(request),
        }
        return render(self.request, self.template_name, data)

class CompanyEndView(View):
    template_name = 'account/company/end.html'
    title = '企業アカウントの作成'

    def post(self, request, **kwargs):
        if request.POST.get("id"):
            company = AuthCompany.objects.filter(display_id=request.POST.get("id"), status=1).first()
            company.status = 2
            company.save()

            if request.POST.get('head_image') and ';base64,' in request.POST.get('head_image'):
                format, imgstr = request.POST.get('head_image').split(';base64,') 
                ext = format.split('/')[-1] 
                head_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                head_image = request.POST.get('head_image')
            if request.POST.get('manager_image') and ';base64,' in request.POST.get('manager_image'):
                format, imgstr = request.POST.get('manager_image').split(';base64,') 
                ext = format.split('/')[-1] 
                manager_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                manager_image = request.POST.get('manager_image')
            if request.POST.get('company_logo_image') and ';base64,' in request.POST.get('company_logo_image'):
                format, imgstr = request.POST.get('company_logo_image').split(';base64,') 
                ext = format.split('/')[-1] 
                company_logo_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                company_logo_image = request.POST.get('company_logo_image')

            if request.POST.get('head_manager_check') == 'on':
                company_profile = CompanyProfile.objects.create(
                    id = str(uuid.uuid4()),
                    company = company,
                    head_family_name = request.POST.get('head_family_name'),
                    head_first_name = request.POST.get('head_first_name'),
                    head_family_name_kana = request.POST.get('head_family_name_kana'),
                    head_first_name_kana = request.POST.get('head_first_name_kana'),
                    head_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    head_email = request.POST.get('head_email'),
                    head_image = head_image,
                    manager_family_name = request.POST.get('head_family_name'),
                    manager_first_name = request.POST.get('head_first_name'),
                    manager_family_name_kana = request.POST.get('head_family_name_kana'),
                    manager_first_name_kana = request.POST.get('head_first_name_kana'),
                    manager_department = '代表者',
                    manager_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    manager_email = request.POST.get('head_email'),
                    manager_image = head_image,
                    company_name = request.POST.get('company_name'),
                    company_postcode = request.POST.get('company_postcode').replace('-', ''),
                    company_prefecture = Prefecture.objects.filter(name=request.POST.get('company_prefecture')).first(),
                    company_address = request.POST.get('company_address'),
                    company_url = request.POST.get('company_url'),
                    company_phone_number = request.POST.get('company_phone_number').replace('-', ''),
                    company_work_parent = WorkParent.objects.filter(value=request.POST.get('company_work_parent_value')).first(),
                    company_work_child = WorkChild.objects.filter(value=request.POST.get('company_work_child_value')).first(),
                    company_logo_image = company_logo_image,
                )
            else:
                company_profile = CompanyProfile.objects.create(
                    id = str(uuid.uuid4()),
                    company = company,
                    head_family_name = request.POST.get('head_family_name'),
                    head_first_name = request.POST.get('head_first_name'),
                    head_family_name_kana = request.POST.get('head_family_name_kana'),
                    head_first_name_kana = request.POST.get('head_first_name_kana'),
                    head_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    head_email = request.POST.get('head_email'),
                    head_image = head_image,
                    manager_family_name = request.POST.get('manager_family_name'),
                    manager_first_name = request.POST.get('manager_first_name'),
                    manager_family_name_kana = request.POST.get('manager_family_name_kana'),
                    manager_first_name_kana = request.POST.get('manager_first_name_kana'),
                    manager_department = request.POST.get('manager_department'),
                    manager_phone_number = request.POST.get('manager_phone_number').replace('-', ''),
                    manager_email = request.POST.get('manager_email'),
                    manager_image = manager_image,
                    company_name = request.POST.get('company_name'),
                    company_postcode = request.POST.get('company_postcode').replace('-', ''),
                    company_prefecture = Prefecture.objects.filter(name=request.POST.get('company_prefecture')).first(),
                    company_address = request.POST.get('company_address'),
                    company_url = request.POST.get('company_url'),
                    company_phone_number = request.POST.get('company_phone_number').replace('-', ''),
                    company_work_parent = WorkParent.objects.filter(value=request.POST.get('company_work_parent_value')).first(),
                    company_work_child = WorkChild.objects.filter(value=request.POST.get('company_work_child_value')).first(),
                    company_logo_image = company_logo_image,
                )

            for i in range(int(request.POST.get('tag_count'))):
                if request.POST.get('tag_genre_'+str(i+1)) and request.POST.get('tag_'+str(i+1)):
                    if HeadTagGenre.objects.filter(name=request.POST.get('tag_genre_'+str(i+1))).exists():
                        tag_genre = HeadTagGenre.objects.filter(name=request.POST.get('tag_genre_'+str(i+1))).first()
                    else:
                        tag_genre = HeadTagGenre.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, HeadTagGenre),
                            name = request.POST.get('tag_genre_'+str(i+1)),
                            count = 0,
                        )
                    if HeadTag.objects.filter(genre=tag_genre, name=request.POST.get('tag_'+str(i+1))).exists():
                        tag = HeadTag.objects.filter(genre=tag_genre, name=request.POST.get('tag_'+str(i+1))).first()
                    else:
                        tag_genre.count = tag_genre.count + 1
                        tag_genre.save()

                        tag = HeadTag.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, HeadTag),
                            genre = tag_genre,
                            name = request.POST.get('tag_'+str(i+1)),
                        )
                    
                    CompanyHashTag.objects.create(
                        id = str(uuid.uuid4()),
                        company = company,
                        number = (i+1),
                        tag = tag,
                    )
            
            if env('EMAIL_DATA'):
                subject = '【アトエル】企業の新規アカウント登録がありました'
                message = get_company_message(self, request, company, company_profile)
                send_mail(subject, message, settings.EMAIL_HOST_USER, [env('EMAIL_DATA')])

            data = {
                'title': self.title,
                'status': 0,
            }
            return render(self.request, self.template_name, data)

        data = {
            'title': self.title,
            'status': 1,
        }
        return render(self.request, self.template_name, data)



class ShopView(View):
    template_name = 'account/shop/index.html'
    title = '店舗アカウントの作成'

    def get(self, request, **kwargs):
        shop = None
        if request.GET.get("id"):
            shop = AuthShop.objects.filter(display_id=request.GET.get("id"), status=1).first()

        data = {
            'title': self.title,
            'shop': shop,
            'country_list': Country.objects.order_by('number').all(),
            'prefecture_list': Prefecture.objects.order_by('number').all(),
        }
        return render(self.request, self.template_name, data)

    def post(self, request, **kwargs):
        shop = None
        if request.POST.get("id"):
            shop = AuthShop.objects.filter(display_id=request.POST.get("id"), status=1).first()

        data = {
            'title': self.title,
            'shop': shop,
            'input': get_shop_data(request),
            'country_list': Country.objects.order_by('number').all(),
            'prefecture_list': Prefecture.objects.order_by('number').all(),
        }
        return render(self.request, self.template_name, data)

class ShopCheckView(View):
    template_name = 'account/shop/check.html'
    title = '店舗アカウントの作成'

    def post(self, request, **kwargs):
        data = {
            'title': self.title,
            'input': get_shop_data(request),
        }
        return render(self.request, self.template_name, data)

class ShopEndView(View):
    template_name = 'account/shop/end.html'
    title = '店舗アカウントの作成'

    def post(self, request, **kwargs):
        if request.POST.get("id"):
            shop = AuthShop.objects.filter(display_id=request.POST.get("id"), status=1).first()
            shop.status = 2
            shop.save()

            if request.POST.get('account_image') and ';base64,' in request.POST.get('account_image'):
                format, imgstr = request.POST.get('account_image').split(';base64,') 
                ext = format.split('/')[-1] 
                account_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                account_image = request.POST.get('account_image')
            if request.POST.get('head_image') and ';base64,' in request.POST.get('head_image'):
                format, imgstr = request.POST.get('head_image').split(';base64,') 
                ext = format.split('/')[-1] 
                head_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                head_image = request.POST.get('head_image')
            if request.POST.get('manager_image') and ';base64,' in request.POST.get('manager_image'):
                format, imgstr = request.POST.get('manager_image').split(';base64,') 
                ext = format.split('/')[-1] 
                manager_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                manager_image = request.POST.get('manager_image')
            if request.POST.get('shop_logo_image') and ';base64,' in request.POST.get('shop_logo_image'):
                format, imgstr = request.POST.get('shop_logo_image').split(';base64,') 
                ext = format.split('/')[-1] 
                shop_logo_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                shop_logo_image = request.POST.get('shop_logo_image')

            if request.POST.get('head_manager_check') == 'on':
                shop_profile = ShopProfile.objects.create(
                    id = str(uuid.uuid4()),
                    shop = shop,
                    account_name = request.POST.get('account_name'),
                    account_image = account_image,
                    account_country = Country.objects.filter(number=request.POST.get('account_country_value')).first(),
                    head_family_name = request.POST.get('head_family_name'),
                    head_first_name = request.POST.get('head_first_name'),
                    head_family_name_kana = request.POST.get('head_family_name_kana'),
                    head_first_name_kana = request.POST.get('head_first_name_kana'),
                    head_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    head_email = request.POST.get('head_email'),
                    head_image = head_image,
                    manager_family_name = request.POST.get('head_family_name'),
                    manager_first_name = request.POST.get('head_first_name'),
                    manager_family_name_kana = request.POST.get('head_family_name_kana'),
                    manager_first_name_kana = request.POST.get('head_first_name_kana'),
                    manager_department = '代表者',
                    manager_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    manager_email = request.POST.get('head_email'),
                    manager_image = head_image,
                    shop_name = request.POST.get('shop_name'),
                    shop_postcode = request.POST.get('shop_postcode').replace('-', ''),
                    shop_prefecture = Prefecture.objects.filter(name=request.POST.get('shop_prefecture')).first(),
                    shop_address = request.POST.get('shop_address'),
                    shop_url = request.POST.get('shop_url'),
                    shop_phone_number = request.POST.get('shop_phone_number').replace('-', ''),
                    shop_logo_image = shop_logo_image,
                )
            else:
                shop_profile = ShopProfile.objects.create(
                    id = str(uuid.uuid4()),
                    shop = shop,
                    account_name = request.POST.get('account_name'),
                    account_image = account_image,
                    account_country = Country.objects.filter(number=request.POST.get('account_country_value')).first(),
                    head_family_name = request.POST.get('head_family_name'),
                    head_first_name = request.POST.get('head_first_name'),
                    head_family_name_kana = request.POST.get('head_family_name_kana'),
                    head_first_name_kana = request.POST.get('head_first_name_kana'),
                    head_phone_number = request.POST.get('head_phone_number').replace('-', ''),
                    head_email = request.POST.get('head_email'),
                    head_image = head_image,
                    manager_family_name = request.POST.get('manager_family_name'),
                    manager_first_name = request.POST.get('manager_first_name'),
                    manager_family_name_kana = request.POST.get('manager_family_name_kana'),
                    manager_first_name_kana = request.POST.get('manager_first_name_kana'),
                    manager_department = request.POST.get('manager_department'),
                    manager_phone_number = request.POST.get('manager_phone_number').replace('-', ''),
                    manager_email = request.POST.get('manager_email'),
                    manager_image = manager_image,
                    shop_name = request.POST.get('shop_name'),
                    shop_postcode = request.POST.get('shop_postcode').replace('-', ''),
                    shop_prefecture = Prefecture.objects.filter(name=request.POST.get('shop_prefecture')).first(),
                    shop_address = request.POST.get('shop_address'),
                    shop_url = request.POST.get('shop_url'),
                    shop_phone_number = request.POST.get('shop_phone_number').replace('-', ''),
                    shop_logo_image = shop_logo_image,
                )
            
            for i in range(int(request.POST.get('tag_count'))):
                if request.POST.get('tag_genre_'+str(i+1)) and request.POST.get('tag_'+str(i+1)):
                    if CompanyTagGenre.objects.filter(name=request.POST.get('tag_genre_'+str(i+1))).exists():
                        tag_genre = CompanyTagGenre.objects.filter(name=request.POST.get('tag_genre_'+str(i+1))).first()
                    else:
                        tag_genre = CompanyTagGenre.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, CompanyTagGenre),
                            company = shop.company,
                            name = request.POST.get('tag_genre_'+str(i+1)),
                            count = 0,
                        )
                    if CompanyTag.objects.filter(genre=tag_genre, name=request.POST.get('tag_'+str(i+1))).exists():
                        tag = CompanyTag.objects.filter(genre=tag_genre, name=request.POST.get('tag_'+str(i+1))).first()
                    else:
                        tag_genre.count = tag_genre.count + 1
                        tag_genre.save()

                        tag = CompanyTag.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, CompanyTag),
                            genre = tag_genre,
                            name = request.POST.get('tag_'+str(i+1)),
                        )
                    
                    ShopHashTag.objects.create(
                        id = str(uuid.uuid4()),
                        shop = shop,
                        number = (i+1),
                        tag = tag,
                    )
            
            if env('EMAIL_DATA'):
                subject = '【アトエル】店舗の新規アカウント登録がありました'
                message = get_shop_message(self, request, shop, shop_profile)
                send_mail(subject, message, settings.EMAIL_HOST_USER, [env('EMAIL_DATA')])

            data = {
                'title': self.title,
                'status': 0,
            }
            return render(self.request, self.template_name, data)

        data = {
            'title': self.title,
            'status': 1,
        }
        return render(self.request, self.template_name, data)



def get_company_data(request):
    tag = list()
    for i in range(int(request.POST.get('tag_count'))):
        tag.append({
            'genre_name': request.POST.get('tag_genre_'+str(i+1)),
            'name': request.POST.get('tag_'+str(i+1)),
        })
    input_data = {
        'id': request.POST.get('id'),
        'head': {
            'family_name': request.POST.get('head_family_name'),
            'first_name': request.POST.get('head_first_name'),
            'family_name_kana': request.POST.get('head_family_name_kana'),
            'first_name_kana': request.POST.get('head_first_name_kana'),
            'phone_number': request.POST.get('head_phone_number'),
            'email': request.POST.get('head_email'),
            'image_name': request.POST.get('head_image_name'),
            'image': request.POST.get('head_image'),
        },
        'manager': {
            'check': request.POST.get('head_manager_check'),
            'family_name': request.POST.get('manager_family_name'),
            'first_name': request.POST.get('manager_first_name'),
            'family_name_kana': request.POST.get('manager_family_name_kana'),
            'first_name_kana': request.POST.get('manager_first_name_kana'),
            'department': request.POST.get('manager_department'),
            'phone_number': request.POST.get('manager_phone_number'),
            'email': request.POST.get('manager_email'),
            'image_name': request.POST.get('manager_image_name'),
            'image': request.POST.get('manager_image'),
        },
        'company': {
            'name': request.POST.get('company_name'),
            'postcode': request.POST.get('company_postcode'),
            'prefecture': request.POST.get('company_prefecture'),
            'prefecture_value': request.POST.get('company_prefecture_value'),
            'address': request.POST.get('company_address'),
            'url': request.POST.get('company_url'),
            'phone_number': request.POST.get('company_phone_number'),
            'work_parent': request.POST.get('company_work_parent'),
            'work_parent_value': request.POST.get('company_work_parent_value'),
            'work_child': request.POST.get('company_work_child'),
            'work_child_value': request.POST.get('company_work_child_value'),
            'logo_image_name': request.POST.get('company_logo_image_name'),
            'logo_image': request.POST.get('company_logo_image'),
        },
        'tag': {
            'count': int(request.POST.get('tag_count')),
            'data': tag,
        },
    }
    return input_data

def get_shop_data(request):
    tag = list()
    for i in range(int(request.POST.get('tag_count'))):
        tag.append({
            'genre_name': request.POST.get('tag_genre_'+str(i+1)),
            'name': request.POST.get('tag_'+str(i+1)),
        })
    input_data = {
        'id': request.POST.get('id'),
        'account': {
            'name': request.POST.get('account_name'),
            'image_name': request.POST.get('account_image_name'),
            'image': request.POST.get('account_image'),
            'country': request.POST.get('account_country'),
            'country_value': request.POST.get('account_country_value'),
        },
        'head': {
            'family_name': request.POST.get('head_family_name'),
            'first_name': request.POST.get('head_first_name'),
            'family_name_kana': request.POST.get('head_family_name_kana'),
            'first_name_kana': request.POST.get('head_first_name_kana'),
            'phone_number': request.POST.get('head_phone_number'),
            'email': request.POST.get('head_email'),
            'image_name': request.POST.get('head_image_name'),
            'image': request.POST.get('head_image'),
        },
        'manager': {
            'check': request.POST.get('head_manager_check'),
            'family_name': request.POST.get('manager_family_name'),
            'first_name': request.POST.get('manager_first_name'),
            'family_name_kana': request.POST.get('manager_family_name_kana'),
            'first_name_kana': request.POST.get('manager_first_name_kana'),
            'department': request.POST.get('manager_department'),
            'phone_number': request.POST.get('manager_phone_number'),
            'email': request.POST.get('manager_email'),
            'image_name': request.POST.get('manager_image_name'),
            'image': request.POST.get('manager_image'),
        },
        'shop': {
            'name': request.POST.get('shop_name'),
            'postcode': request.POST.get('shop_postcode'),
            'prefecture': request.POST.get('shop_prefecture'),
            'prefecture_value': request.POST.get('shop_prefecture_value'),
            'address': request.POST.get('shop_address'),
            'url': request.POST.get('shop_url'),
            'phone_number': request.POST.get('shop_phone_number'),
            'logo_image_name': request.POST.get('shop_logo_image_name'),
            'logo_image': request.POST.get('shop_logo_image'),
        },
        'tag': {
            'count': int(request.POST.get('tag_count')),
            'data': tag,
        },
    }
    return input_data

def get_company_message(self, request, company, company_profile):
    protocol = 'https' if self.request.is_secure() else 'http'
    site = get_current_site(self.request)

    if env('NGROK'):
        url = env('NGROK_URL')
    else:
        url = env('DOMAIN_URL')
    
    message = '企業の新規アカウント登録がありました\n'
    message += '\n'
    message += '■企業ページ\n'
    message += protocol + '://' + site.domain + '/head/company/detail/?id=' + str(company.display_id) + '\n'
    message += '\n'
    message += '【代表者情報】\n'
    message += '氏名 : ' + company_profile.head_family_name + ' ' + company_profile.head_first_name + '\n'
    message += 'フリガナ : ' + company_profile.head_family_name_kana + ' ' + company_profile.head_first_name_kana + '\n'
    message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(company_profile.head_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
    message += 'メールアドレス : ' + company_profile.head_email + '\n'
    if company_profile.head_image:
        message += 'プロフィール画像 : ' + url + company_profile.head_image.url + '\n'
    else:
        message += 'プロフィール画像 : \n'
    message += '\n'
    message += '【担当者情報】\n'
    if request.POST.get('head_manager_check') == 'on':
        message += '代表者と同一\n'
    else:
        message += '氏名 : ' + company_profile.manager_family_name + ' ' + company_profile.manager_first_name + '\n'
        message += 'フリガナ : ' + company_profile.manager_family_name_kana + ' ' + company_profile.manager_first_name_kana + '\n'
        message += '所属部署 : ' + company_profile.manager_department + '\n'
        message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(company_profile.manager_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
        message += 'メールアドレス : ' + company_profile.manager_email + '\n'
        if company_profile.manager_image:
            message += 'プロフィール画像 : ' + url + company_profile.manager_image.url + '\n'
        else:
            message += 'プロフィール画像 : \n'
    message += '\n'
    message += '【会社情報】\n'
    message += '会社名 : ' + company_profile.company_name + '\n'
    message += '郵便番号 : ' + str(company_profile.company_postcode)[0:3] + '-' + str(company_profile.company_postcode)[3:7] + '\n'
    message += '住所 : ' + company_profile.company_prefecture.name + company_profile.company_address + '\n'
    message += 'URL : ' + company_profile.company_url + '\n'
    message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(company_profile.company_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
    message += '大業種 : ' + company_profile.company_work_parent.name + '\n'
    message += '小業種 : ' + company_profile.company_work_child.name + '\n'
    if company_profile.company_logo_image:
        message += 'ロゴ画像 : ' + url + company_profile.company_logo_image.url + '\n'
    else:
        message += 'ロゴ画像 : \n'
    if CompanyHashTag.objects.filter(company=company).exists():
        message += '\n'
        message += 'タグ\n'
        for tag_item in CompanyHashTag.objects.filter(company=company).all():
            message += 'ジャンル : ' + tag_item.tag.genre.name + ' / タグ名 : ' + tag_item.tag.name + '\n'

    return message

def get_shop_message(self, request, shop, shop_profile):
    protocol = 'https' if self.request.is_secure() else 'http'
    site = get_current_site(self.request)

    if env('NGROK'):
        url = env('NGROK_URL')
    else:
        url = env('DOMAIN_URL')

    message = '店舗の新規アカウント登録がありました\n'
    message += '\n'
    message += '■店舗ページ\n'
    message += protocol + '://' + site.domain + '/company/shop/detail/?id=' + str(shop.display_id) + '\n'
    message += '\n'
    message += '【アトエルアカウント情報】\n'
    message += 'アカウント名 : ' + shop_profile.head_family_name + ' ' + shop_profile.head_first_name + '\n'
    if shop_profile.account_image:
        message += 'アカウント画像 : ' + url + shop_profile.account_image.url + '\n'
    else:
        message += 'アカウント画像 : \n'
    message += '会社・事業者の所在国・地域 : ' + shop_profile.account_country.name + '\n'
    message += '\n'
    message += '【代表者情報】\n'
    message += '氏名 : ' + shop_profile.head_family_name + ' ' + shop_profile.head_first_name + '\n'
    message += 'フリガナ : ' + shop_profile.head_family_name_kana + ' ' + shop_profile.head_first_name_kana + '\n'
    message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(shop_profile.head_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
    message += 'メールアドレス : ' + shop_profile.head_email + '\n'
    if shop_profile.head_image:
        message += 'プロフィール画像 : ' + url + shop_profile.head_image.url + '\n'
    else:
        message += 'プロフィール画像 : \n'
    message += '\n'
    message += '【担当者情報】\n'
    if request.POST.get('head_manager_check') == 'on':
        message += '代表者と同一\n'
    else:
        message += '氏名 : ' + shop_profile.manager_family_name + ' ' + shop_profile.manager_first_name + '\n'
        message += 'フリガナ : ' + shop_profile.manager_family_name_kana + ' ' + shop_profile.manager_first_name_kana + '\n'
        message += '所属部署 : ' + shop_profile.manager_department + '\n'
        message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(shop_profile.manager_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
        message += 'メールアドレス : ' + shop_profile.manager_email + '\n'
        if shop_profile.manager_image:
            message += 'プロフィール画像 : ' + url + shop_profile.manager_image.url + '\n'
        else:
            message += 'プロフィール画像 : \n'
    message += '\n'
    message += '【会社情報】\n'
    message += '会社名 : ' + shop_profile.shop_name + '\n'
    message += '郵便番号 : ' + str(shop_profile.shop_postcode)[0:3] + '-' + str(shop_profile.shop_postcode)[3:7] + '\n'
    message += '住所 : ' + shop_profile.shop_prefecture.name + shop_profile.shop_address + '\n'
    message += 'URL : ' + shop_profile.shop_url + '\n'
    message += '電話番号 : ' + phonenumbers.format_number(phonenumbers.parse(shop_profile.shop_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) + '\n'
    if shop_profile.shop_logo_image:
        message += 'ロゴ画像 : ' + url + shop_profile.shop_logo_image.url + '\n'
    else:
        message += 'ロゴ画像 : \n'
    if ShopHashTag.objects.filter(shop=shop).exists():
        message += '\n'
        message += 'タグ\n'
        for tag_item in ShopHashTag.objects.filter(shop=shop).all():
            message += 'ジャンル : ' + tag_item.tag.genre.name + ' / タグ名 : ' + tag_item.tag.name + '\n'

    return message