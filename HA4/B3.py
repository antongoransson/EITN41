from hashlib import sha1
from binascii import unhexlify,hexlify

def i_to_b(i, size=1):
    return i.to_bytes(size,byteorder='big')

def h_to_b(h):
    return unhexlify(h)

def b_to_h(b):
    return hexlify(b).decode('utf-8')

def I2OSP(x, xLen):
    return  i_to_b(x, xLen)

def OAEP_encode(M, seed, k = 128, hLen = 20):
    lHash = sha1().digest()
    PS = i_to_b(0)* (k - len(M) // 2 - 2 * hLen - 2)
    DB = lHash  + PS + i_to_b(1) +  h_to_b(M)
    dbMask = MGF1(seed, k- hLen - 1)
    maskedDB = bytes(a ^ b for a, b in zip(h_to_b(dbMask), DB))
    seedMask = MGF1(b_to_h(maskedDB), hLen)
    maskedSeed = bytes(a ^ b for a, b in zip(h_to_b(seed), h_to_b(seedMask)))
    EM = i_to_b(0) +  maskedSeed + maskedDB
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

def MGF1(mgfSeed, maskLen):
    mgfSeed = h_to_b(mgfSeed)
    T = b''
    i = 0
    while len(T) < maskLen:
         C = I2OSP(i, 4)
         i += 1
         T += sha1(mgfSeed + C).digest()
    return b_to_h(T[:maskLen])

mgfSeed = "0123456789abcdef" #(hexadecimal) 8 bytes
maskLen = 30 #(decimal)30 byte
encoded = MGF1(mgfSeed, maskLen)
M = "fd5507e917ecbe833878"
seed = "1e652ec152d0bfcd65190ffc604c0933d0423381"
EM = ("0000255975c743f5f11ab5e450825d93b52a160aeef9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51f40e13fb29ed5101dbcb044e6232e6371935c8347286db25c9ee20351ee82")
print("Encode corr",OAEP_encode(M, seed) == EM)
dc_M = OAEP_decode(EM)
print("Decode corr", dc_M == M )
# print((encoded))

mgfSeed = "9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214"
maskLen = 21 
encoded = MGF1(mgfSeed, maskLen)
print("Encoded", encoded)
M = "c107782954829b34dc531c14b40e9ea482578f988b719497aa0687"
seed = "1e652ec152d0bfcd65190ffc604c0933d0423381"
EM = "0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f"
print("Encode ",OAEP_encode(M, seed))
dc_M = OAEP_decode(EM)
print("Decode ", dc_M )
