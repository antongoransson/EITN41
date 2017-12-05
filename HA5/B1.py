from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5
from binascii import unhexlify, hexlify



def h_bytes(h):
    return bytearray(unhexlify(h)) # converts string to byte_array

def b_to_h(b):
    return hexlify(b).decode('utf-8')

def h_str(x):
    return format(x, 'x')

def byte(x, size=None):
    if size is None:
        size = (x.bit_length() + 7) // 8
    return x.to_bytes(size, 'big')

def h_int(h):
    return int(h, 16)

def b_int(b):
    return int.from_bytes(b, byteorder='big')

def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  x, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = extendex_euc_alg(b, n)
    if g == 1:
        return x % n

def decrypt_message(m, pem_f):
    key = RSA.importKey(open(pem_f, "rb").read())
    e = key.e
    p = key.p
    q = key.q
    d = mulinv(e, (p-1)*(q-1))
    raw_cipher_data = b64decode(m)
    private_key = RSA.construct((p * q, e, d, p, q))
    cipher = PKCS1_v1_5.new(private_key)
    message = cipher.decrypt(raw_cipher_data, "")
    print(message.decode('utf8').strip())

key1 = 'testKey.pem'
m1= "T9FAfFVcVCdPH45kv3OU/Kot9NOyQ2t5tWI1GW6nJ4Ul435T68wq1f1vm3KhDcKONzdN3krJ/VwlIzdssIcqmVizw5mnMupmd1gNmf7EKLZWjT4LaMQhDMijrfhxCdbiQKjKqYnUehlOCeDS0JXOJpiYcCtbmTVYHBmxBuOZ1l8="
key = 'key.pem'
m = "Qe7+h9OPQ7PN9CmF0ZOmD32fwpJotrUL67zxdRvhBn2U3fDtoz4iUGRXNOxwUXdJ2Cmz7zjS0DE8ST5dozBysByz/u1H//iAN+QeGlFVaS1Ee5a/TZilrTCbGPWxfNY4vRXHP6CB82QxhMjQ7/x90/+JLrhdAO99lvmdNetGZjY="
decrypt_message(m1, key1)
