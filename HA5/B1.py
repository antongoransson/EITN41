from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode


def decrypt_message(m, pem_f):
    c_key = RSA.importKey(open(pem_f, 'rb').read())
    e, p, q, d = [getattr(c_key, s) for s in ['e', 'p', 'q', 'd']]
    n = p * q
    decoded_data = b64decode(m)
    private_key = RSA.construct((n, e, d, p, q))
    sentinel = Random.new().read(15)
    cipher = PKCS1_v1_5.new(private_key)
    message = cipher.decrypt(decoded_data,sentinel)
    return message.decode('utf8').strip()

if __name__ == '__main__':
    key = input('Key: ')
    m = input('Message: ')
    if key == '' or m == '':
        key = 'key.pem'
        m = 'Qe7+h9OPQ7PN9CmF0ZOmD32fwpJotrUL67zxdRvhBn2U3fDtoz4iUGRXNOxwUXdJ2Cmz7zjS0DE8ST5dozBysByz/u1H//iAN+QeGlFVaS1Ee5a/TZilrTCbGPWxfNY4vRXHP6CB82QxhMjQ7/x90/+JLrhdAO99lvmdNetGZjY='
        key = 'testKey.pem'
        m= 'T9FAfFVcVCdPH45kv3OU/Kot9NOyQ2t5tWI1GW6nJ4Ul435T68wq1f1vm3KhDcKONzdN3krJ/VwlIzdssIcqmVizw5mnMupmd1gNmf7EKLZWjT4LaMQhDMijrfhxCdbiQKjKqYnUehlOCeDS0JXOJpiYcCtbmTVYHBmxBuOZ1l8='
    d_message = decrypt_message(m, key)
    print(d_message)
