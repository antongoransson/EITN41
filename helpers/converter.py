import hashlib
import binascii

def int_to_bytes(intNbr, size = None, byteorder='big'):
    if(size is None):
        size = intNbr.bit_length() + 7
    byte_array = (intNbr).to_bytes(size, byteorder=byteorder)
    return byte_array

def hex_to_int(hexDecStr):
    return int(hexDecStr, 16)

def int_to_hex(integer):
    return hex(integer)

def hex_to_bytes(hexStr):
    return binascii.unhexlify(hexStr) # converts string to byte_array

def bytes_to_hex(byte_array):
    hex_data = binascii.hexlify(byte_array)
    return  hex_data.decode('utf-8')

def bytes_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

def sha1_hash_bytes_array(byte_array, size = None):
    if(type(byte_array) is int):
        byte_array = int_to_bytes(byte_array, size)
    if(type(byte_array) is not bytes):
        raise Exception("Input needs to be of type bytes")
    hash_object = hashlib.sha1(byte_array)
    return hash_object.digest()
