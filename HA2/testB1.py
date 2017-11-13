import unittest
from B1 import *

class TestB1(unittest.TestCase):

    def test_B1_someone_else_sends_message(self):
        SA = 'BF0D'
        DA = '186F'
        SB = '3C99'
        DB = '2EAD'
        M = '62AB'
        b = 0
        broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
        print("Broadcast:", broadcast)
        self.assertEqual(broadcast, "8394B556")

    def test_B1_i_send_message(self):
        SA = 'D75C'
        SB = 'EE87'
        DA = 'C568'
        DB = 'FCB3'
        M = '4674'
        b = 1
        broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
        print("Broadcast:", broadcast)
        self.assertEqual(broadcast, "7FAF")

    def test_B1_no_one_sends_message(self):
        SA = '75F5'
        SB = 'B1AC'
        DA = '67C1'
        DB = 'A398'
        M = '00BC'
        b = 0
        broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
        print("Broadcast:", broadcast)
        self.assertEqual(broadcast, "C4590000")

    def test_B1_i_send_message_1(self):
        SA = '27C2'
        SB = '0879'
        DA = '35F6'
        DB = '1A4D'
        M = '27BC'
        b = 1
        broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
        print("Broadcast:", broadcast)
        self.assertEqual(broadcast, "0807")

    def test_B1_someone_else_sends_message_1(self):
        SA = '0C73'
        SB = '80C1'
        DA = 'A2A9'
        DB = '92F5'
        M = '9B57'
        b = 0
        broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
        print("Broadcast:", broadcast)
        self.assertEqual(broadcast, "8CB2BCEE")

if __name__ == '__main__':
    unittest.main()
