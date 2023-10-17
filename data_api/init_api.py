import os

from data_api.utils import generate_rsa_keypair, gen_rsa_pkcs8


# 对应ecs服务的环境变量
os.environ['resource_name'] = 'wf'
os.environ['resource_secret'] = 'asidhu123bbkbkj2bi34i2u3b4b'

# rsa_key = generate_rsa_keypair()
# private_key = rsa_key['private_key'].export_key()
# public_key = rsa_key['public_key'].export_key()

rsa_key = gen_rsa_pkcs8()
os.environ['private_key'] = rsa_key['private_key'].decode('utf-8')
os.environ['public_key'] = rsa_key['public_key'].decode('utf-8')
print(os.environ['private_key'])
print(os.environ['public_key'])

