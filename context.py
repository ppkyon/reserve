
from sign.models import AuthUser, ManagerProfile

import environ

env = environ.Env()
env.read_env('.env')

def env_data(request):
    site_name = env('SITE_NAME')
    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")

    data = {
        'env_site_name': site_name,
    }
    return data

def header_data(request):
    manager = None
    if not request.user.is_anonymous:
        manager = AuthUser.objects.filter(id=request.user.id).first()
        manager.profile = ManagerProfile.objects.filter(manager=manager).first()

    data = {
        'header_manager': manager
    }
    return data