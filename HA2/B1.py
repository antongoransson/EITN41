from operator import xor
from converter import *
import binascii

def dc_broadcast(secretA, secretB, dataA, dataB, message, b):
    if(b == 1):
        myBroadcast = hex_to_int(dataA) ^ hex_to_int(dataB) ^ hex_to_int(message)
        myBroadcast = int_to_hex(myBroadcast)[2:].zfill(4)
    else:
        myData = hex_to_int(secretA) ^ hex_to_int(secretB)
        myBroadcast = hex_to_int(dataA) ^ hex_to_int(dataB) ^ myData
        myBroadcast = int_to_hex((myData))[2:] + int_to_hex(myBroadcast)[2:].zfill(4)
    return myBroadcast.upper()
