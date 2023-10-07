import os
import time
import hashlib
import traceback
from datetime import datetime, timezone, timedelta
from typing import Optional, Union, List, Tuple

import jwt
from fastapi import FastAPI, Query, Path, Request, Header, Depends
from fastapi.responses import Response, JSONResponse, HTMLResponse

from data_api import init_api


resource_name = os.environ['resource_name']
resource_secret = os.environ['resource_secret']
public_key = resource_secret


# print(resource_name, resource_secret)

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


def unverified_response(description):
    return JSONResponse(
        status_code=403, 
        content = {
            'success': False,
            'error': {
                'code': 'Authentication failed.', 
                'reason': f'You have no permission to access this resource. {description}'},
            'response': {}
        }
    )

def verify_token(token: str=Header(None, convert_underscores=False)) -> bool:

    # print('token', token, type(token))
    if token is None:
        return unverified_response('no token')

    digest = sha256(resource_secret)
    try:
        de_token = jwt.decode(token, key=digest, algorithms=['HS256'])
        # print(de_token)
        return True
    except jwt.ExpiredSignatureError as e:
        # traceback.print_exc()
        # print('expired token')
        return unverified_response('expired token')
    except jwt.InvalidTokenError:
        # print('invalid token')
        # traceback.print_exc()
        return unverified_response('invalid token')


def verify_token_rs256(token: str=Header(None, convert_underscores=False)) -> bool:

    # print('token', token, type(token))
    if token is None:
        return unverified_response('no token')

    try:
        de_token = jwt.decode(token, key=public_key, algorithms=['RS256'])
        # print(de_token)
        return True
    except jwt.ExpiredSignatureError as e:
        # traceback.print_exc()
        # print('expired token')
        return unverified_response('expired token')
    except jwt.InvalidTokenError:
        # print('invalid token')
        # traceback.print_exc()
        return unverified_response('invalid token')


@app.get("/")
async def frontpage():
    return HTMLResponse(status_code=200, content='''
        <h1>Welcome to use! <a href='docs/'>help docs</a></h1>
    ''')


@app.get("/weather_forecast")
async def main(*,
    lon: float=Query(default=..., ge=-180, le=180),
    lat: float=Query(default=..., ge=-90, le=90),
    hours: Optional[int]=Query(default=7*24, ge=0, le=7*24),
    verify=Depends(verify_token)
    ):
    '''
    Args:\n
        lon: 经度 degree
        lat: 纬度 degree
        hours: 请求的预测数据的时间长度, 最大为7天

    Returns:\n
        Response
    '''

    return JSONResponse(
        status_code=200, 
        content = {
            'success': True,
            'error': 'null',
            'response': {'lon': lon, 'lat': lat, 'hours': hours}
        }
    )


if __name__ == '__main__':
    # uvicorn data_api.main:app --host 0.0.0.0 --port 5555 --reload
    pass
