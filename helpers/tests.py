import unittest

from converter import *


# >>> import binascii
# >>> binascii.hexlify(bytearray(array_alpha))
# '8535eaf1'
class TestConverter(unittest.TestCase):


    def test_intToBytes(self):
        byteArray = intToByteArray(intNbr=500, size=4,  byteorder='big')
        string = sha1HashByteArray(byteArray)
        self.assertEqual("c6c5da207269aa4a59743ded27105b13bc8dd384", string)

    def test_stringToInt(self):
        result = hexDecToInt("fedcba9876543210")
        hashResult = sha1HashInt(result, 8)
        a = intToHexDec(2897)
        byteArray = intToByteArray(intNbr=2897, size=4,  byteorder='big')
        f = byteArrayToHex (byteArray)
        print(f)
        print(hashResult)
        intResult = hexDecToInt(hashResult)
        self.assertEqual(18364758544493064720, result)
        self.assertEqual(946229717077375328329532411653585908948565005770, intResult)



if __name__ == '__main__':
    unittest.main()
