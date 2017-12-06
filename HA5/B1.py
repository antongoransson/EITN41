from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode

def construct_key(key):
    c_key = RSA.importKey(open(key, 'rb').read())
    e, p, q, d = [getattr(c_key, s) for s in ['e', 'p', 'q', 'd']]
    n = p * q
    return  RSA.construct((n, e, d, p, q))

def decrypt_message(m, priv_key):
    decoded_data = b64decode(m)
    sentinel = Random.new().read(15)
    cipher = PKCS1_v1_5.new(priv_key)
    message = cipher.decrypt(decoded_data, sentinel)
    return message.decode('utf8').strip()

def censored_RSA(m, key):
    priv_key = construct_key(key)
    decrypted_msg = decrypt_message(m, priv_key)
    return decrypted_msg

if __name__ == '__main__':
    key = input('Key: ')
    m = input('Message: ')
    if key == '' or m == '':
        key = 'inputs/key.pem'
        m = 'Qe7+h9OPQ7PN9CmF0ZOmD32fwpJotrUL67zxdRvhBn2U3fDtoz4iUGRXNOxwUXdJ2Cmz7zjS0DE8ST5dozBysByz/u1H//iAN+QeGlFVaS1Ee5a/TZilrTCbGPWxfNY4vRXHP6CB82QxhMjQ7/x90/+JLrhdAO99lvmdNetGZjY='
        # key = 'inputs/testKey.pem'
        # m= 'T9FAfFVcVCdPH45kv3OU/Kot9NOyQ2t5tWI1GW6nJ4Ul435T68wq1f1vm3KhDcKONzdN3krJ/VwlIzdssIcqmVizw5mnMupmd1gNmf7EKLZWjT4LaMQhDMijrfhxCdbiQKjKqYnUehlOCeDS0JXOJpiYcCtbmTVYHBmxBuOZ1l8='
    decrypted_msg = censored_RSA(m,key)
    print(decrypted_msg)
