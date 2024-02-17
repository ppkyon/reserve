from sign.models import CompanyProfile, ShopProfile, AuthLogin
from table.models import TableSearch, TableNumber, TableSort

import environ

env = environ.Env()
env.read_env('.env')

def side_data(request):
    image = None
    name = None

    if not request.user.is_anonymous:
        auth_login = AuthLogin.objects.filter(user=request.user).first()
        if auth_login:
            if '/company/' in request.path:
                company = auth_login.company
                company_profile = CompanyProfile.objects.filter(company=company).first()
                if company_profile:
                    image = company_profile.company_logo_image.url
                    name = company_profile.company_name
            elif not '/head/' in request.path:
                shop = auth_login.shop
                shop_profile = ShopProfile.objects.filter(shop=shop).first()
                if shop_profile:
                    image = shop_profile.shop_logo_image.url
                    name = shop_profile.shop_name
        
    data = {
        'side_logo_image': image,
        'side_logo_name': name,
    }
    return data