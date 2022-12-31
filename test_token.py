'''
测试认证授权过程：
    - 客户端：使用get请求token（生产环境使用安全方式post，https）
    - 认证服务器：验证请求，返回jwt token
    - 客户端：使用token请求数据
    - 资源服务器：验证token，返回数据
'''



import base64
import hashlib
import os



def gen_credential(client_id, client_secret):
    credential = "{0}:{1}".format(client_id, client_secret)
    credential = base64.b64encode(credential.encode("utf-8"))
    print(credential)
    return credential


def sha256(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha256 = hashlib.sha256(salt)   # add salt
    else:
        sha256 = hashlib.sha256()   # add salt
    sha256.update(secret.encode('utf-8'))
    digest = sha256.hexdigest()
    print(digest, sha256)
    return digest


gen_credential(
    'tpA75lGkmCrjOci8PzcAX0ZHH4HnBdjfYTv0Do1y',
    'uZlzW44d6ie98xgSfQcy9OZWKjQnZe0vU7WPkG52Cun1sWF4lV3pMjqvCxOdUjp7pb46DKsJ2Fcj33kql8TK73V1mVGDg0GkNBX4sEPt8N2PtdcmVIgmC7db5SFdYlBE'
)
# dHBBNzVsR2ttQ3JqT2NpOFB6Y0FYMFpISDRIbkJkamZZVHYwRG8xeTp1Wmx6VzQ0ZDZpZTk4eGdTZlFjeTlPWldLalFuWmUwdlU3V1BrRzUyQ3VuMXNXRjRsVjNwTWpxdkN4T2RVanA3cGI0NkRLc0oyRmNqMzNrcWw4VEs3M1YxbVZHRGcwR2tOQlg0c0VQdDhOMlB0ZGNtVklnbUM3ZGI1U0ZkWWxCRQ==


