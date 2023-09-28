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
    credential = base64.b64encode(credential.encode("utf-8")).decode("utf-8")
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
    结合django-oauth-toolkit使用
    '''
    def init_para(self):
        self.client_name = None
        self.client_id = None
        self.client_secret = None
        self.scope = None
        self.token_type = None
        self.grant_type = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.init_para()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.init_para()

        self.url_info = request.META.get('PATH_INFO', False)
        print('JWTMiddleware middleware in', self.url_info)
        if self.url_info == '/o/token/':
            try:
                request_body_dict = {}
                for i in request.body.decode().split('&'):
                    request_body_dict[i.split('=')[0]] = i.split('=')[1]
                self.grant_type = request_body_dict['grant_type']
                self.token_type = request_body_dict['token_type']
                print("Request data:", request_body_dict)
            except:
                print('error load body')
            
            if self.grant_type == 'client_credentials':
                # 客户端模式
                print('client mode')
                self.resource_name = request_body_dict.get('resource_name', None)
                self.client_id = request_body_dict.get('client_id', None)
                self.client_secret = request_body_dict.get('client_secret', None)
                if self.resource_name:
                    credential = gen_authorization(self.client_id, self.client_secret)
                    headers = request.headers
                    headers_temp = vars(headers)
                    headers_temp['Authorization'] = f"Basic {credential}"
                    headers_temp['Content-Type'] = 'application/x-www-form-urlencoded'
                    headers_temp['Cache-Control'] = 'no-cache'
                    setattr(request, 'headers', headers_temp)
                else:
                    return HttpResponse(json.dumps({'error': 'header缺少resource_name'}), status_code=400)
            elif self.grant_type == 'password':
                # 密码模式
                print('password mode')
                try:
                    self.resource_name = request_body_dict.get('resource_name')
                    self.client_id = request_body_dict.get('client_id', None)
                    self.client_secret = request_body_dict.get('client_secret', None)
                    self.username = request_body_dict.get('username', None)
                    self.password = request_body_dict.get('password', None)
                except:
                    return HttpResponse(json.dumps({'error': 'header缺少resource_name'}), status_code=400)
            else:
                return HttpResponse(json.dumps({'error': 'grant_type error'}))
        
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        print('JWTMiddleware middleware out')
        if response.status_code == 200:
            if self.token_type == 'jwt':
                print('jwt token')
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


class SimpleJWTMiddleware(MiddlewareMixin):
    '''
    结合djangorestframework-simplejwt使用
    '''
    def init_para(self):
        self.client_name = None
        self.client_id = None
        self.client_secret = None
        self.scope = None
        self.token_type = None
        self.grant_type = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.init_para()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.init_para()

        self.url_info = request.META.get('PATH_INFO', False)
        print('SimpleJWTMiddleware middleware in', self.url_info)
        if self.url_info == '/api/token/':
            try:
                request_body_dict = json.loads(request.body)
            except:
                return HttpResponse(json.dumps({'error': 'load body error'}))
            
            self.grant_type = request_body_dict.get('grant_type', None)
            if self.grant_type == 'client_credentials':
                # 客户端模式
                print('client mode')
                # self.resource_name = request_body_dict.get('resource_name', None)
                # self.client_id = request_body_dict.get('client_id', None)
                # self.client_secret = request_body_dict.get('client_secret', None)
                # if self.resource_name:
                #     credential = gen_authorization(self.client_id, self.client_secret)
                #     headers = request.headers
                #     headers_temp = vars(headers)
                #     headers_temp['Authorization'] = f"Basic {credential}"
                #     headers_temp['Content-Type'] = 'application/x-www-form-urlencoded'
                #     headers_temp['Cache-Control'] = 'no-cache'
                #     setattr(request, 'headers', headers_temp)
                # else:
                #     return HttpResponse(json.dumps({'error': 'header缺少resource_name'}), status_code=400)
            elif self.grant_type == 'password':
                # 密码模式
                print('password mode')
                # TODO: 
                # 1 在这里将username替换成用户表中的id,用户使用username,内部验证使用id
                # 2 验证用户是否关联了资源服务器,即是否能获取到用户指定的资源服务器的权限,权限信息在用户表中,一旦授权,
                #   该用户能够凭借授权token访问权限内的所有资源(所有资源服务器的id保存在jwt token的payload中),
                #   资源服务器验证token,用户不需要在请求中指定获取哪个资源服务器的token
                try:
                    self.resource_name = request_body_dict['resource_name']
                    self.client_id = request_body_dict['client_id']
                    self.username = request_body_dict['username']
                    self.password = request_body_dict['password']

                except:
                    return HttpResponse(json.dumps({'error': 'header缺少resource_name'}))
            else:
                return HttpResponse(json.dumps({'error': 'grant_type error'}))
        
        # print(request.headers)
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        print('SimpleJWTMiddleware middleware out')
        if response.status_code == 200:
            if self.token_type == 'jwt':
                print('jwt token')
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

