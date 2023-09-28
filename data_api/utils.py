import string
import random
import datetime

import jwt
from Crypto.PublicKey import RSA


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

    rsa_key = generate_rsa_keypair()
    private_key = rsa_key['private_key'].export_key()
    public_key = rsa_key['public_key'].export_key()
    print(private_key)
    print(public_key)

    encoded_jwt = encode_jwt(payload, private_key)
    print(encoded_jwt)


    decoded_jwt = decode_jwt(encoded_jwt, public_key)
    print(decoded_jwt)





