import copy
import hashlib
import base64
import json
import traceback
from datetime import datetime, timedelta

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import oauth2_provider
from oauth2_provider.models import get_application_model, Application
import jwt


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
    - 确认请求为获取token请求
    - 收集生成JWT token的数据
    - 生成token返回
    '''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.is_query_token = False
        self.client_name = None
        self.client_id = None
        self.client_secret = None
        self.scope = None

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.user_name = request.META.get('username', False)
        self.url_info = request.META.get('PATH_INFO', False)
        if self.url_info == '/o/token/':
            self.is_query_token = True
            self.client_name = request.META.get('HTTP_CLIENT_NAME', False)
            if self.client_name:
                try:
                    client = Application.objects.get(name=self.client_name)
                except:
                    print('获取client信息出错')
                    print(traceback.format_exc())
                    return HttpResponse({'error': '获取client信息出错'})
                
                self.client_id = client.client_id
                self.client_secret = client.client_secret
                credential = gen_authorization(self.client_id, self.client_secret)
                
                headers = request.headers
                headers_temp = vars(headers)
                headers_temp['Authorization'] = f"Basic {credential}"
                setattr(request, 'header', headers_temp)
                
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        if self.is_query_token:
            digest = sha256(self.client_secret)
            jwt_token = gen_jwt_token(digest, expire_minute=20, token_data={
                'client_name': self.client_name,
                'scope': self.scope
            })

            jwt_content = json.dumps({
                "access_token": jwt_token,
                "token_type": "JWT"
            })
            setattr(response, 'content', jwt_content)

        return response
