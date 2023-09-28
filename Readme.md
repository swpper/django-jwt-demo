# 说明
- 这是一个django jwt 认证的demo
- 角色和场景: 
    - 用户: 认证服务器,资源服务器,用户. 
    - 场景: 用户在认证服务器注册,资源服务器在认证服务器注册,目前只考虑资源服务被认证服务器拥有,用户通过认证服务器获取授权token,然后向资源服务器获取内容.
- 方案支持:
    - django + django-oauth-toolkit: 原生client_credentials和password token以及client_credentials和password的jwt token
    - django + django-rest-framework-simplejwt: 原生password token以及password的jwt token(支持添加自定义payload)
- 关于token: 支持生成token和验证token,刷新token和销毁token未改动.

# 使用示例

## create python env
```python
# create python env by `venv`
python venv <env-name>

# activate env
# mac or linux
source <env-name>/bin/activate

# windows
<env-name>\Scripts\activate

# install python packages
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## create django project
- create user data: `python access_model.py`

## run django and api service
```python
# run django
python manage.py runserver 8080

# run api service
uvicorn data_api.main:app --host 0.0.0.0 --port 5555 --reload
```

## customer get token

```bash
# get token
# django-oauth-toolkit
# get token by client_credentials
# origin token
curl --location 'http://127.0.0.1:8080/o/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: csrftoken=KTfQufLtbChMy8xfk5lI6RIsywhDB6k9' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'token_type=token' \
--data-urlencode 'client_id=gjJgLLKeEx1XCNlOODDXlRf5BXk19OH3OZX4RguE' \
--data-urlencode 'client_secret=9KH4Qddl1ngXjx84PWIytXtmEbo4NoOs58E8aliySqVvzqP1pmiVzULN7Cand21BEnnR1EgghPO8iNfoWd09ucsxhQky3Ks0gMY8j2W3J7tI4dcjIqAX7F6iJVEE7Mhq' \
--data-urlencode 'resource_name=wf'

# jwt token
curl --location 'http://127.0.0.1:8080/o/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: csrftoken=KTfQufLtbChMy8xfk5lI6RIsywhDB6k9' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'token_type=jwt' \
--data-urlencode 'client_id=gjJgLLKeEx1XCNlOODDXlRf5BXk19OH3OZX4RguE' \
--data-urlencode 'client_secret=9KH4Qddl1ngXjx84PWIytXtmEbo4NoOs58E8aliySqVvzqP1pmiVzULN7Cand21BEnnR1EgghPO8iNfoWd09ucsxhQky3Ks0gMY8j2W3J7tI4dcjIqAX7F6iJVEE7Mhq' \
--data-urlencode 'resource_name=wf'

# get token by password
# origin token
curl --location 'http://127.0.0.1:8080/o/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: csrftoken=KTfQufLtbChMy8xfk5lI6RIsywhDB6k9' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'token_type=token' \
--data-urlencode 'client_id=H4jfey8GBgq9dcyfgRyyjnnOLbzuU4cfXg3FNFd2' \
--data-urlencode 'client_secret=EWFoJAWZ0cYb9esP52s4jS7pKkBnTadMUHpXSDPbwZFxX0YRnhSp5rdToQleiBjoXqSyV4Le01rKTKxxEcasiCnZd1TenwDDhCT0zitcyLInLIp61vYOiMhHmdJeopNr' \
--data-urlencode 'resource_name=wf' \
--data-urlencode 'username=customer8' \
--data-urlencode 'password=customer8'

# jwt token
curl --location 'http://127.0.0.1:8080/o/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: csrftoken=KTfQufLtbChMy8xfk5lI6RIsywhDB6k9' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'token_type=jwt' \
--data-urlencode 'client_id=H4jfey8GBgq9dcyfgRyyjnnOLbzuU4cfXg3FNFd2' \
--data-urlencode 'client_secret=EWFoJAWZ0cYb9esP52s4jS7pKkBnTadMUHpXSDPbwZFxX0YRnhSp5rdToQleiBjoXqSyV4Le01rKTKxxEcasiCnZd1TenwDDhCT0zitcyLInLIp61vYOiMhHmdJeopNr' \
--data-urlencode 'resource_name=wf' \
--data-urlencode 'username=customer8' \
--data-urlencode 'password=customer8'


# django-rest-framework-simplejwt
# get token by password
```bash
curl --location 'http://127.0.0.1:8080/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "customer8",
    "password": "customer8",
    "grant_type": "password",
    "token_type": "token",
    "resource_name": "wf",
    "client_id": "abc"
}'


# get resource
# api只支持jwt token
# 目前只测试了django-oauth-toolkit的jwt token,使用resource_secret对称加密
curl --location 'http://0.0.0.0:5555/weather_forecast?lon=111&lat=12&hours=144' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTU4ODM4NDEsImV4cCI6MTY5NTg4NTA0MSwiZGF0YSI6eyJjbGllbnRfaWQiOiJINGpmZXk4R0JncTlkY3lmZ1J5eWpubk9MYnp1VTRjZlhnM0ZORmQyIiwicmVzb3VyY2VfbmFtZSI6IndmIiwic2NvcGUiOm51bGx9fQ.HRFYKN8txi_zdPjBnbrH2tULyNcZRDRqzu6pUJE6cFU'

# response
{
    "success": true,
    "error": "null",
    "response": {
        "lon": 111.0,
        "lat": 12.0,
        "hours": 144
    }
}

```

# 关键的点
- django-oauth-toolkit的secret加密算法可以通过settings设置,默认为`pbkdf2_sha256`,包括application的client_secret和用户密码,自定义创建的用户密码需要使用`pbkdf2_sha256`算法手动转换存入.认证的时候使用加密前的.


# Todo
1 确定resource表和application的区别，在这里两者的作用是一样的, 在django-oauth-toolkit中使用application,
其他地方应该不能使用，所以resource表是必要的
2 引入非对称密钥
    - django-oauth-toolkit使用资源服务器的私钥加密生成jwt
    - django-rest-framework-simplejwt使用资源服务器的私钥加密生成jwt