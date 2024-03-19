from django.http import JsonResponse

from fixture.models import Prefecture
from sign.models import AuthLogin, AuthCompany, AuthShop, CompanyProfile
from tag.models import HeadTag, CompanyHashTag

from common import get_model_field

import phonenumbers

def get_profile(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    company = AuthCompany.objects.filter(id=auth_login.shop.company.id).values(*get_model_field(AuthCompany)).first()
    company['profile'] = CompanyProfile.objects.filter(company=auth_login.shop.company).values(*get_model_field(CompanyProfile)).first()
    company['prefecture'] = Prefecture.objects.filter(id=company['profile']['company_prefecture']).values(*get_model_field(Prefecture)).first()
    company['phone_number'] = phonenumbers.format_number(phonenumbers.parse(company['profile']['company_phone_number'], 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
    company['display_date'] = company['created_at'].strftime('%Y年%m月%d日 %H:%M')

    tag_list = list()
    for company_tag_item in CompanyHashTag.objects.filter(company=auth_login.shop.company).order_by('number').all():
        tag_list.append( HeadTag.objects.filter(id=company_tag_item.tag.id).values(*get_model_field(HeadTag)).first())
    company['tag'] = tag_list
    return JsonResponse( {'company': company}, safe=False )