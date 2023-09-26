import re
import hashlib
import base64
import json
import traceback
from datetime import datetime, timedelta

import jwt
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from oauth2_provider.models import get_application_model, Application
from datacenter.models import Resource


Application = get_application_model()


def gen_authorization(client_id, client_secret):
    credential = "{0}:{1}".format(client_id, client_secret)
    credential = base64.b64encode(credential.encode("utf-8"))
    return credential


def sha256(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha256 = hashlib.sha256(salt)   # add salt
    else:
        sha256 = hashlib.sha256()
    sha256.update(secret.encode('utf-8'))
    digest = sha256.hexdigest()
    return digest


def gen_jwt_token(secret, expire_minute: int=10, token_data: dict={}) -> str:
    token = jwt.encode(
        {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=expire_minute),
            'data': token_data
        },
        secret,
        algorithm='HS256'
    )
    return token


class JWTMiddleware(MiddlewareMixin):
    '''
    替换o/token路径的默认的token
    '''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.is_query_token = False
        self.client_name = None
        self.client_id = None
        self.client_secret = None
        self.scope = None
        self.token_type = None
        self.grant_type = None

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.url_info = request.META.get('PATH_INFO', False)
        print(self.url_info)
        if self.url_info == '/o/token/':
            request_data = json.loads(request.body)
            self.grant_type = request_data.get('grant_type', None)
            self.token_type = request_data.get('token_type', None)
            print("Request data:", request_data)
            
            print(self.grant_type)
            print(self.token_type)
            if self.grant_type == 'client_credentials':
                # 客户端模式
                self.is_query_token = True
                self.resource_name = request_data.get('HTTP_RESOURCE_NAME', None)
                self.client_id = request_data.get('HTTP_RESOURCE_NAME', None)
                self.client_secret = request_data.get('HTTP_RESOURCE_NAME', None)

                if self.resource_name:
                    credential = gen_authorization(self.client_id, self.client_secret)
                    headers = request.headers
                    headers_temp = vars(headers)
                    headers_temp['Authorization'] = f"Basic {credential}"
                    setattr(request, 'header', headers_temp)
                else:
                    return HttpResponse({'error': 'header缺少resource_name'})
            if self.grant_type == 'password':
                # 密码模式
                self.is_query_token = True
                self.resource_name = request_data.get('HTTP_RESOURCE_NAME', None)
        else:
            return HttpResponse({'error': 'header缺少grant_type'})

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        if response.status_code == 200:
            if self.token_type == 'jwt':
                try:
                    resource = Resource.objects.filter(resource_name=self.resource_name)[0]
                except:
                    print('获取resource信息出错')
                    print(traceback.format_exc())
                    setattr(response, 'content', json.dumps({'error': 500}))
                    setattr(response, 'status_code', 500)
                    return response
                
                digest = sha256(resource.resource_secret)
                jwt_token = gen_jwt_token(digest, expire_minute=20, token_data={
                    'client_id': self.client_id,
                    'resource_name': self.resource_name,
                    'scope': self.scope
                })

                jwt_content = json.dumps({
                    "access_token": jwt_token,
                    "token_type": "JWT"
                })
                setattr(response, 'content', jwt_content)

        return response
