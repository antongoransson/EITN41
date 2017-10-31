import hashlib
import binascii
import unittest

def int_to_bytes(int_nbr, size = None, byteorder='big'):
    if(size is None):
        size = int_nbr.bit_length() + 7
    byte_array = (int_nbr).to_bytes(size, byteorder=byteorder)
    return byte_array

def hex_to_int(hex_str):
    return int(hex_str, 16)

def int_to_hex(integer):
    return hex(integer)

def hex_to_bytes(hex_str):
    return binascii.unhexlify(hex_str) # converts string to byte_array

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
