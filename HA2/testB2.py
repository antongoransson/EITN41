import unittest
from B2 import *

class TestB2(unittest.TestCase):

    def test_B2_1(self):
        sender_ip = '159.237.13.37'
        mix_ip = '94.147.150.188'
        m = 2
        file_path = 'inputs/B2_cia.log.1337.pcap'
        ip_sum = find_partners(sender_ip, mix_ip, m, file_path)
        print("SUM: ", ip_sum)
        self.assertEqual(ip_sum, 6100595791)

    def test_B2_2(self):
        sender_ip = '161.53.13.37'
        mix_ip = '11.192.206.171'
        m = 12
        file_path = 'inputs/B2_cia.log.1339.pcap'
        ip_sum = find_partners(sender_ip, mix_ip, m, file_path)
        print("SUM: ", ip_sum)
        self.assertEqual(ip_sum, 28979912646)

if __name__ == '__main__':
    unittest.main()
