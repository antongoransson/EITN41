from math import ceil
from hashlib import sha1
from binascii import unhexlify,hexlify

# mgfSeed  seed from which mask is generated, an octet string
#maskLen  intended length in octets of the mask, at most 2^32 hLen
# hash =  20 bytes
def OAEP_encode(M, seed):
    pass
def MGF1(mgfSeed, maskLen):
    mgfSeed = unhexlify(mgfSeed)
    T = b''
    i = 0
    while len(T) < maskLen:
         C = I2OSP (i, 4)
         i += 1
         T = T + sha1(mgfSeed + C).digest()
    print("T", T[:maskLen*2])
    return T[:maskLen]

def I2OSP(x, xLen):
    return  unhexlify(hex(x)[2:].zfill(xLen*2))

mgfSeed = "0123456789abcdef" #(hexadecimal) 8 bytes
maskLen = 30 #(decimal)30 byte
encoded = MGF1(mgfSeed, maskLen)
print(hexlify(encoded))
