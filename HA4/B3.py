from hashlib import sha1
from binascii import unhexlify,hexlify
from sys import argv

def i_to_b(i, size=1):
    return i.to_bytes(size,byteorder='big')

def h_to_b(h):
    return unhexlify(h)

def b_to_h(b):
    return hexlify(b).decode('utf-8')

def I2OSP(x, xLen):
    X = []
    for i in range(xLen):
        X.append(x % 256)
        x //= 256
    return bytes(X[::-1])

def OAEP_encode(M, seed, k = 128, hLen = 20):
    lHash = sha1().digest()
    PS = I2OSP(0, k - len(M) // 2 - 2 * hLen - 2)
    DB = lHash  + PS + I2OSP(1, 1) +  h_to_b(M)
    dbMask = MGF1(seed, k- hLen - 1)
    maskedDB = bytes(a ^ b for a, b in zip(h_to_b(dbMask), DB))
    seedMask = MGF1(b_to_h(maskedDB), hLen)
    maskedSeed = bytes(a ^ b for a, b in zip(h_to_b(seed), h_to_b(seedMask)))
    EM = I2OSP(0, 1) +  maskedSeed + maskedDB
    return b_to_h(EM)

def OAEP_decode(EM, k = 128, hLen = 20):
    EM = h_to_b(EM)
    maskedSeed = EM[1:hLen + 1]
    maskedDB = EM[hLen + 1:]
    seedMask = MGF1(b_to_h(maskedDB), hLen)
    seed = bytes(a ^ b for a, b in zip(maskedSeed, h_to_b(seedMask)))
    dbMask = MGF1(b_to_h(seed), k - hLen - 1)
    DB = bytes(a ^ b for a, b in zip(h_to_b(dbMask), maskedDB))[hLen:]
    M = DB[DB.index(1) + 1:]
    return b_to_h(M)

def MGF1(mgfSeed, maskLen, Hash=sha1):
    mgfSeed = h_to_b(mgfSeed)
    T = b''
    i = 0
    while len(T) < maskLen:
         C = I2OSP(i, 4)
         i += 1
         T += Hash(mgfSeed + C).digest()
    return b_to_h(T[:maskLen])

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
