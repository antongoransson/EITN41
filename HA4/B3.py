from hashlib import sha1
from math import ceil
from binascii import unhexlify, hexlify
from sys import argv

def to_byte(h):
    return unhexlify(h)

def to_hex(b):
    return hexlify(b).decode('utf-8')

def I2OSP(x, xLen):
    X = []
    for i in range(xLen):
        X.append(x % 256)
        x //= 256
    return bytes(X[::-1])

def OAEP_encode(M, seed, k = 128, hLen = 20, L="", Hash=sha1):
    lHash = Hash(L.encode('utf8')).digest()
    PS = I2OSP(0, k - len(M) // 2 - 2 * hLen - 2)
    DB = lHash  + PS + I2OSP(1, 1) +  to_byte(M)
    dbMask = MGF1(seed, k- hLen - 1)
    maskedDB = bytes(a ^ b for a, b in zip(to_byte(dbMask), DB))
    seedMask = MGF1(to_hex(maskedDB), hLen)
    maskedSeed = bytes(a ^ b for a, b in zip(to_byte(seed), to_byte(seedMask)))
    EM = I2OSP(0, 1) +  maskedSeed + maskedDB
    return to_hex(EM)

def OAEP_decode(EM, k = 128, hLen = 20):
    EM = to_byte(EM)
    maskedSeed = EM[1:hLen + 1]
    maskedDB = EM[hLen + 1:]
    seedMask = MGF1(to_hex(maskedDB), hLen)
    seed = bytes(a ^ b for a, b in zip(maskedSeed, to_byte(seedMask)))
    dbMask = MGF1(to_hex(seed), k - hLen - 1)
    DB = bytes(a ^ b for a, b in zip(to_byte(dbMask), maskedDB))[hLen:]
    index = DB.index(1) + 1
    M = DB[index:]
    return to_hex(M)

def MGF1(mgfSeed, maskLen, hLen = 20, Hash=sha1):
    mgfSeed = to_byte(mgfSeed)
    T = b''
    for i in range(ceil(maskLen / hLen)):
         C = I2OSP(i, 4)
         T += Hash(mgfSeed + C).digest()
    return to_hex(T[:maskLen])

if __name__ == '__main__':
    if len(argv) == 2:
        mgfSeed = input('').split("=")[1]
        maskLen = int(input('').split("=")[1])
        MG = MGF1(mgfSeed, maskLen)
        M = input('').split("=")[1]
        seed = input('').split("=")[1]
        ec_M = OAEP_encode(M, seed)
        EM = input('').split("=")[1]
        dc_M = OAEP_decode(EM)
    else:
        mgfSeed = input('mgfSeed: ')
        maskLen = int(input('maskLen: '))
        MG = MGF1(mgfSeed, maskLen)
        M = input('M: ')
        seed = input('seed: ')
        ec_M = OAEP_encode(M, seed)
        EM = input('EM: ')
        dc_M = OAEP_decode(EM)
    print("MGF1:", MG)
    print("\nEM:", ec_M)
    print("\nDM:",dc_M)
