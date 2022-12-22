import os
import time
import hashlib
import traceback
from datetime import datetime, timezone, timedelta
from typing import Optional, Union, List, Tuple

import jwt
from fastapi import FastAPI, Query, Path, Request, Header
from fastapi.responses import Response, JSONResponse, HTMLResponse

from data_api import init_api


resource_name = os.environ['resource_name']
resource_secret = os.environ['resource_secret']

print(resource_name, resource_secret)

app = FastAPI()


def sha256(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha256 = hashlib.sha256(salt)   # add salt
    else:
        sha256 = hashlib.sha256()   # add salt
    sha256.update(secret.encode('utf-8'))
    digest = sha256.hexdigest()
    return digest


def check_auth(token) -> bool:

    print('token', token, type(token))
    if token is None:
        return False

    # 尝试用jwt解析
    digest = sha256(resource_secret)
    try:
        de_token = jwt.decode(token, key=digest, algorithms=['HS256'])
        print(de_token)
    except jwt.ExpiredSignatureError as e:
        traceback.print_exc()
        print('token 过期')
        return False
    except jwt.InvalidTokenError:
        print('token 无效')
        traceback.print_exc()
        return False

    return True


@app.get("/")
async def frontpage():
    return HTMLResponse(status_code=200, content='''
        <h1>Welcome to use! <a href='docs/'>help docs</a></h1>
    ''')


@app.get("/weather_forecast")
async def main(*,
    # source: Source,
    # resolution: Resolution,
    # elements: Optional[List[Element]]=Query(default=None),
    # obs_time: Optional[str]=Query(default=None, regex=r'[\d{8}T\d{6}|None]'),
    # time: str=Query(default=..., regex=r'\d{8}T\d{6}'),
    lon: float=Query(default=..., ge=-180, le=180),
    lat: float=Query(default=..., ge=-90, le=90),
    hours: Optional[int]=Query(default=7*24, ge=0, le=7*24),
    token: Optional[str]=Header(None, convert_underscores=False)
    ):
    '''
    Args:\n
        lon: 经度 degree
        lat: 纬度 degree
        hours: 请求的预测数据的时间长度，最大为7天

    Returns:\n
        Response
    '''

    if check_auth(token):
        return JSONResponse(
            status_code=200, 
            content = {
                'success': True,
                'error': 'null',
                'response': {'lon': lon, 'lat': lat, 'hours': hours}
            }
        )
    else:
        # 任何验证失败均返回以下错误信息
        return JSONResponse(
            status_code=403, 
            content = {
                'success': False,
                'error': {
                    'code': 'Authentication failed.', 
                    'reason': 'You have no permission to access this resource.'},
                'response': {}
            }
        )
    


if __name__ == '__main__':
    # uvicorn data_api.main:app --host 0.0.0.0 --port 5555 --reload
    pass
