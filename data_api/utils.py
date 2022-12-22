import string
import random



def gen_random_secret(n: int=20):
    candidate_chars = string.digits + string.ascii_letters
    secret = ''
    for i in range(n):
        secret += random.choice(candidate_chars)
    return secret