from django.db import models

import datetime
import itertools
import string
import random
import uuid

def create_code(dig, model, other_models=[]):
    code_list = model.objects.values_list('display_id', flat=True)

    other_code_list = []
    if other_models:
        for m in other_models:
            other_code_list.append(m.objects.values_list('display_id', flat=True))
        other_code_list = itertools.chain.from_iterable(other_code_list)
    
    min = 10 ** (dig - 1)
    max = 10 ** dig - 1
    while True:
        code = random.randint(min, max)
        if code not in code_list and code not in other_code_list:
            break

    return code

def create_token():
    return uuid.uuid4().hex

def create_password():
    random_list = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    return ''.join(random_list)

def create_expiration_date(hours):
    now = datetime.datetime.now()
    return now + datetime.timedelta(hours=hours)



def get_model_field(model, old=False):
    if old:
        field_list = list()
        for field_index, field_value in enumerate(model._meta.get_fields()):
            field_list.append(field_value.name)
        return field_list
    else:
        meta_fields = model._meta.get_fields()
        filtered_fields = filter(
            lambda x: not isinstance(x, models.ManyToOneRel),
            meta_fields
        )
        meta_field_names = map(lambda x: x.name, filtered_fields)
        return list(meta_field_names)