import os
import time
import traceback
from collections import namedtuple
from datetime import datetime, timezone, timedelta
from typing import Optional, Union, List, Tuple

import jwt
from fastapi import FastAPI, Query, Path, Request, Header, Depends
from fastapi.responses import Response, JSONResponse, HTMLResponse

from data_api import init_api
from data_api.utils import sha256


resource_name = os.environ['resource_name']
resource_secret = os.environ['resource_secret']
# print(resource_name, resource_secret)
digest = sha256(resource_secret)

public_key = os.environ['public_key']
private_key = os.environ['private_key']
print(private_key)

app = FastAPI()

VERIFY_RESULT = namedtuple('VERIFY_RESULT', ['is_success', 'reason_str'])


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

def verify_token(Authorization: str=Header(None, convert_underscores=False)) -> VERIFY_RESULT:
    token = Authorization
    if token is None:
        return VERIFY_RESULT(False, 'no token')
    token_type = token.split(' ')[0]
    token_body = token.split(' ')[1]
    print('token_type', token_type, 'token_body', token_body)
    if token_type != 'Bearer':
        return VERIFY_RESULT(False, 'token type is not Bearer')
    
    try:
        de_token = jwt.decode(token_body, key=digest, algorithms=['HS256'])
        print(de_token)
        if resource_name == de_token['resource_name']:
            return VERIFY_RESULT(True, 'null')
        else:
            return VERIFY_RESULT(False, 'invalid resource')
    except jwt.ExpiredSignatureError as e:
        # traceback.print_exc()
        # print('expired token')
        return VERIFY_RESULT(False, 'expired token')
    except jwt.InvalidTokenError:
        # print('invalid token')
        # traceback.print_exc()
        return VERIFY_RESULT(False, 'invalid token')
    

def verify_token_rs256(Authorization: str=Header(None, convert_underscores=False)) -> bool:
    token = Authorization
    if token is None:
        return VERIFY_RESULT(False, 'no token')
    token_type = token.split(' ')[0]
    token_body = token.split(' ')[1]
    print('token_type', token_type, 'token_body', token_body)
    if token_type != 'Bearer':
        return VERIFY_RESULT(False, 'token type is not Bearer')

    try:
        de_token = jwt.decode(token_body, key=public_key, algorithms=['RS256'])
        if resource_name == de_token['resource_name']:
            return VERIFY_RESULT(True, 'null')
        else:
            return VERIFY_RESULT(False, 'invalid resource')
    except jwt.ExpiredSignatureError as e:
        # traceback.print_exc()
        # print('expired token')
        return VERIFY_RESULT(False, 'expired token')
    except jwt.InvalidTokenError:
        # print('invalid token')
        # traceback.print_exc()
        return VERIFY_RESULT(False, 'invalid token')


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
    # verify: VERIFY_RESULT=Depends(verify_token)
    verify: VERIFY_RESULT=Depends(verify_token_rs256)
    ):
    '''
    Args:\n
        lon: 经度 degree
        lat: 纬度 degree
        hours: 请求的预测数据的时间长度, 最大为7天

    Returns:\n
        Response
    '''
    is_success = verify.is_success
    reason_str = verify.reason_str
    if is_success:
        return JSONResponse(
            status_code=200, 
            content = {
                'success': True,
                'error': 'null',
                'response': {'lon': lon, 'lat': lat, 'hours': hours}
            }
        )
    else:
        return unverified_response(reason_str)


if __name__ == '__main__':
    # uvicorn data_api.main:app --host 0.0.0.0 --port 5555 --reload
    pass
