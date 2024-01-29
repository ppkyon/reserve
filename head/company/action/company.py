from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import get_template

from fixture.models import Prefecture
from sign.models import AuthCompany, CompanyProfile
from tag.models import HeadTag, CompanyHashTag

from common import create_code, get_model_field

import environ
import phonenumbers
import uuid

env = environ.Env()
env.read_env('.env')

def add(request):
    auth_shop = AuthCompany.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, AuthCompany),
        status = 1,
        delete_flg = False,
    )

    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
    else:
        site_name = env('SITE_NAME')
    subject = '【アトエル】企業の新規アカウント登録メール'
    template = get_template('head/company/email/add.txt')
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
    company = AuthCompany.objects.filter(display_id=request.POST.get('id')).first()
    company_profile = CompanyProfile.objects.filter(company=company).first()
    company_profile.head_family_name = request.POST.get('head_family_name')
    company_profile.head_first_name = request.POST.get('head_first_name')
    company_profile.head_family_name_kana = request.POST.get('head_family_name_kana')
    company_profile.head_first_name_kana = request.POST.get('head_first_name_kana')
    company_profile.head_email = request.POST.get('head_email')
    company_profile.company_name = request.POST.get('company_name')
    company_profile.company_postcode = request.POST.get('company_postcode').replace('-', '')
    company_profile.company_prefecture = Prefecture.objects.filter(value=request.POST.get('company_prefecture')).first()
    company_profile.company_address = request.POST.get('company_address')
    company_profile.company_phone_number = request.POST.get('company_phone_number').replace('-', '')
    company_profile.memo = request.POST.get('memo')
    company_profile.save()

    CompanyHashTag.objects.filter(company=company).all().delete()
    if request.POST.get('tag[]'):
        for tag_index, tag_item in enumerate( request.POST.get('tag[]').split(',') ):
            CompanyHashTag.objects.create(
                id = str(uuid.uuid4()),
                company = company,
                number = (tag_index+1),
                tag = HeadTag.objects.filter(display_id=tag_item).first()
            )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )



def get_profile(request):
    company = AuthCompany.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(AuthCompany)).first()
    company['profile'] = CompanyProfile.objects.filter(company__id=company['id']).values(*get_model_field(CompanyProfile)).first()
    company['prefecture'] = Prefecture.objects.filter(id=company['profile']['company_prefecture']).values(*get_model_field(Prefecture)).first()
    company['phone_number'] = phonenumbers.format_number(phonenumbers.parse(company['profile']['company_phone_number'], 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
    company['display_date'] = company['created_at'].strftime('%Y年%m月%d日 %H:%M')

    tag_list = list()
    for shop_tag_item in CompanyHashTag.objects.filter(company__id=company['id']).order_by('number').all():
        tag_list.append( HeadTag.objects.filter(id=shop_tag_item.tag.id).values(*get_model_field(HeadTag)).first())
    company['tag'] = tag_list
    return JsonResponse( {'company': company}, safe=False )