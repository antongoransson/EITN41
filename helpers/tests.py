import unittest
from converter import *

class TestConverter(unittest.TestCase):

    def test_int_to_hex(self):
        int_nbr1 = 500
        int_nbr2 = 2897
        byte_array1 = int_to_bytes(integer = int_nbr1, size = 4)
        byte_array2 = int_to_bytes(integer = int_nbr2, size = 4)
        str1 = bytes_to_hex(byte_array1)
        str2 = bytes_to_hex(byte_array2)

        self.assertEqual("000001f4", str1)
        self.assertEqual("00000b51", str2)

    def test_int_to_bytesHash(self):
        int_nbr = 500
        byte_array = int_to_bytes(integer = int_nbr, size = 4, byteorder='big')
        byte_array_hash = sha1_hash_bytes_array(byte_array)
        self.assertEqual("c6c5da207269aa4a59743ded27105b13bc8dd384", bytes_to_hex(byte_array_hash))

    def test_string_to_int(self):
        byte_result = hex_to_bytes("fedcba9876543210")
        int_result = bytes_to_int(byte_result)
        hash_result = sha1_hash_bytes_array(int_result, size = 8)
        self.assertEqual(18364758544493064720, int_result)
        self.assertEqual(18364758544493064720, hex_to_int("fedcba9876543210"))
        self.assertEqual(946229717077375328329532411653585908948565005770, bytes_to_int(hash_result))

if __name__ == '__main__':
    unittest.main()
