
import json
import hashlib
import jwt
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader

from datacenter.models import Customer, Resource



content_template = {
    'success': True,
    'error': 'null',
    'response': {}
}


def sha1(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha1 = hashlib.sha1(salt)   # add salt
    else:
        sha1 = hashlib.sha1()
    sha1.update(secret.encode('utf-8'))
    digest = sha1.hexdigest()
    return digest


def sha256(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha256 = hashlib.sha256(salt)   # add salt
    else:
        sha256 = hashlib.sha256()   # add salt
    sha256.update(secret.encode('utf-8'))
    digest = sha256.hexdigest()
    return digest


def gen_token(request, exp_minute: int=10) -> str:
    # secret
    resource_name = request.headers['resource_name']
    resource = Resource.objects.get(pk=resource_name)
    secret = resource.resource_secret
    digest = sha256(secret)

    # jwt
    token = jwt.encode(
        {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=exp_minute),
            'data':{
                'resource_name': resource_name
            }
        },
        digest,
        algorithm='HS256'
    )

    return token


def check_query_token_request(request) -> dict:

    customer_name = request.META.get('HTTP_CUSTOMER_NAME', 'unkown')
    customer_secret = request.META.get('HTTP_CUSTOMER_SECRET', 'unkown')
    resource_name = request.META.get('HTTP_RESOURCE_NAME', 'unkown')
    scope = request.META.get('HTTP_SCOPE', 'unkown')

    print(customer_name, customer_secret, resource_name, scope)

    customer = Customer.objects.get(pk=customer_name)

    if customer_secret == customer.customer_secret:
        if resource_name in json.loads(customer.resource_name):
            if scope in json.loads(customer.scope):
                return {'result': True, 'reason': ''}
            else:
                return {'result': False, 'reason': 'Invalid scope.'}
        else:
            return {'result': False, 'reason': 'Invalid resource_id.'}
    else:
        return {'result': False, 'reason': 'Invalid secret.'}


def my_auth(request):
    '''
    检查发出请求header里面的用户信息：用户是否存在，申请认证和权限是否可行
        通过，生成token并返回
        不通过，返回相应的错误信息
    '''
    result = check_query_token_request(request)

    if result['result']:
        content = content_template
        content['response'] = {
            'token': gen_token(request)
        }
        content = json.dumps(content)
        return HttpResponse(status=200, content=content)
    else:
        content = content_template
        content['success'] = False
        content['error'] = result['reason']
        content = json.dumps(content)
        return HttpResponse(status=401, content=content)


def tookit_auth(request):
    
    return HttpResponse('Hello world, tookit_auth')
