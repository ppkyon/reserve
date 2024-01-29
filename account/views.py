from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.shortcuts import render

from django.views.generic import View

from fixture.models import Prefecture, WorkParent, WorkChild
from sign.models import AuthCompany, CompanyProfile
from tag.models import HeadTagGenre, HeadTag, CompanyHashTag

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
            'input': get_input_data(request),
        }
        return render(self.request, self.template_name, data)

class CompanyCheckView(View):
    template_name = 'account/company/check.html'
    title = '企業アカウントの作成'

    def post(self, request, **kwargs):
        data = {
            'title': self.title,
            'input': get_input_data(request),
        }
        return render(self.request, self.template_name, data)

class CompanyEndView(View):
    template_name = 'account/company/end.html'
    title = '企業アカウントの作成'

    def post(self, request, **kwargs):
        company = None
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
                subject = '【アトエル】店舗の新規アカウント登録がありました'
                message = get_message_data(self, request, company, company_profile)
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



def get_input_data(request):
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

def get_message_data(self, request, company, company_profile):
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