import os
import json
import string
import random
from datetime import datetime, timezone, timedelta

import django
import init_django
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from datacenter.models import Customer, Resource


# pwd='4562154'
# mpwd=make_password(pwd,None,'pbkdf2_sha256')  # 创建django密码，第三个参数为加密算法
# pwd_bool=check_password(pwd,mpwd)# 返回的是一个bool类型的值，验证密码正确与否

def bjtznow():
    return datetime.now(tz=timezone(timedelta(hours=8)))

resources = {
    'wf': 'asidhu123bbkbkj2bi34i2u3b4b',
    'lf': 'qwJNQcZfBekzcsmRp9llKjuFvzj'
}
resource_names = list(resources.keys())
scope_base = ['r', 'w']




def init_customer():

#     def gen_random_secret(n: int=8):
#         candidate_chars = string.digits + string.ascii_letters
#         secret = ''
#         for i in range(n):
#             secret += random.choice(candidate_chars)
#         return secret
    
    def gen_combination(origin_list):
        def idx_combination(idx_str, res=[], str_comb=""):
            if len(str_comb) >0 and str_comb not in res:
                res.append(str_comb)
            if len(idx_str) == 0:
                return res
            comb1 = str_comb + '-' + idx_str[0]
            idx_res = idx_combination(idx_str[1:],res,comb1)
            idx_res = idx_combination(idx_str[1:],res, str_comb)
            return idx_res
        
        idx_str = [str(i) for i in range(len(origin_list))]
        idx_all = idx_combination(idx_str, [], '')
        idx_all = [i.strip('-').split('-') for i in idx_all]

        res_all = []
        for i in idx_all:
            temp = []
            for j in i:
                temp.append(origin_list[int(j)])
            res_all.append(temp)
        return res_all

    scope_all = gen_combination(scope_base)
    resources_all = gen_combination(resource_names)

    def generte_cuntomers(n: int=20):
        customers = []
        for i in range(n):
            customers.append({
                'username': f'customer{i}',
                # 'password': gen_random_secret(),
                'password': make_password(f'customer{i}', None, 'pbkdf2_sha256'),
                'email': f'customer{i}@example.com',
                'resource_name': json.dumps(random.choice(resources_all)),
                'scope': json.dumps(random.choice(scope_all)),
                'update_date': bjtznow(),
            
            })
        return customers

    customers = generte_cuntomers()
    for customer in customers:
        print(customer)
        q = Customer(**customer)
        q.save()


def init_resource():
    for i, (name, secret) in enumerate(resources.items()):
        r = Resource(resource_name=name, resource_secret=secret,
            update_date=bjtznow())
        r.save()


if __name__ == '__main__':    
    init_customer()
    # init_resource()