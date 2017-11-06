import unittest
from B1 import *

class TestB3(unittest.TestCase):
    def test_B3_1_find_merkel_root(self):
        file_in = open("inputs/inputB1.txt","r")
        nbrs = get_values_from_file(file_in)
        print("Numbers:", nbrs)
        self.assertEqual(nbrs, "5496331440914992338434701218071555719657419448245128019889398009532562488698540071959143506293615978")
        file_in.close()
        
if __name__ == '__main__':
    unittest.main()
