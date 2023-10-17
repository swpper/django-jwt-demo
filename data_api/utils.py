import string
import random
import hashlib
import datetime

import jwt
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def gen_random_secret(n: int=20):
    candidate_chars = string.digits + string.ascii_letters
    secret = ''
    for i in range(n):
        secret += random.choice(candidate_chars)
    return secret


def generate_rsa_keypair():
    """Generate an RSA keypair."""
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return {'private_key': private_key, 'public_key': public_key}


def gen_rsa_pkcs8():

    # 生成RSA密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 将私钥转换为PKCS8格式
    private_key_pkcs8 = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 将公钥转换为PKCS8格式
    public_key_pkcs8 = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    )
    return {'private_key': private_key_pkcs8, 'public_key': public_key_pkcs8}


def sha256(secret: str, salt='iamsalt'):
    if salt:
        salt = str(salt).encode('utf-8')
        sha256 = hashlib.sha256(salt)   # add salt
    else:
        sha256 = hashlib.sha256()   # add salt
    sha256.update(secret.encode('utf-8'))
    digest = sha256.hexdigest()
    return digest


def encode_jwt(payload, private_key):
    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')
    return encoded_jwt


def decode_jwt(encoded_jwt, public_key):
    decoded_jwt = jwt.decode(encoded_jwt, public_key, algorithms=['RS256'])
    return decoded_jwt




if __name__ == '__main__':
    payload = {
    'sub': '1234567890',
    'name': 'John Doe',
    'iat': datetime.datetime.utcnow(),
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    # rsa_key = generate_rsa_keypair()
    # private_key = rsa_key['private_key'].export_key()
    # public_key = rsa_key['public_key'].export_key()
    # print(private_key)
    # print(public_key)

    # encoded_jwt = encode_jwt(payload, private_key)
    # print(encoded_jwt)


    # decoded_jwt = decode_jwt(encoded_jwt, public_key)
    # print(decoded_jwt)

    rsa_key = gen_rsa_pkcs8()
    print(rsa_key['private_key'].decode('utf-8'))
    print(rsa_key['public_key'].decode('utf-8'))

