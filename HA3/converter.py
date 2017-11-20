import hashlib
import binascii
import unittest

def int_to_bytes(integer, size = None, byteorder='big'):
    if(size is None):
        size = integer.bit_length() + 7
    return bytearray(integer.to_bytes(size, byteorder))

def hex_to_int(hex_str):
    return int(hex_str, 16)

def int_to_hex(integer):
    return hex(integer)

def hex_to_bytes(hex_str):
    return bytearray(binascii.unhexlify(hex_str)) # converts string to byte_array

def bytes_to_hex(byte_array):
    return  binascii.hexlify(byte_array).decode('utf-8')

def bytes_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

def sha1_hash(byte_array, size = None):
    if(type(byte_array) is int):
        byte_array = int_to_bytes(byte_array, size)
    hash_object = hashlib.sha1(byte_array)
    return bytearray(hash_object.digest())
