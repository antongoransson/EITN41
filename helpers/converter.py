import hashlib
from struct import *

def byteArrToHexString(byteArray, byteorder='big'):
    a = ""
    hexa = hex(int.from_bytes(byteArray, byteorder='big'))
    a ="".join( "0" for i in range (len(byteArray)*2+2 - len(hex(int.from_bytes(byteArray, byteorder='big')))))
    print(a + hexa[2:])
    return hex(int.from_bytes(byteArray, byteorder='big'))

def intToByteArray(intNbr, size = None, byteorder='big'):
    if(size is None): #
        size = intNbr.bit_length() + 1
    byteArray = (intNbr).to_bytes(size, byteorder=byteorder)
    return byteArray

def hexDecToInt(hexDecStr):
    return int(hexDecStr, 16)

def intToHexDec(integer):
    return hex(integer)
def byteArrayToHex(byteArray):
    return (''.join('{:02x}'.format(x) for x in byteArray))


def sha1HashByteArray(byteArray):
    hash_object = hashlib.sha1(byteArray)
    return hash_object.hexdigest()

def sha1HashInt(integer, size= None, byteorder='big'):
    if(size is None): #
        size = hexDecInt.bit_length() + 1
    return sha1HashByteArray((integer).to_bytes(size, byteorder=byteorder))
