import unittest
from B3 import *

class TestB3(unittest.TestCase):
    def test_B3_1_find_merkel_root(self):
        file_in = open("inputs/inputB3_1.txt","r")
        root = get_merkle_root(file_in)
        print("Merkle root:", root)
        self.assertEqual(root, "6f51120bc17e224de27d3d27b32f05d0a5ffb376")
        file_in.close()

    def test_B3_1_find_merkel_root2(self):
        file_in = open("inputs/inputB3_1_quiz.txt","r")
        root = get_merkle_root(file_in)
        print("Merkle root:", root)
        self.assertEqual(root,"57252a732982c12a13cc88c66d286acee68b676e")
        file_in.close()

    def test_B3_2_full_node(self):
        file_in = open("inputs/inputB3_2.txt","r")
        root = full_node(file_in)
        print("Merkle path node + root:", root)
        self.assertEqual(root,"R8d3f164890509c6510cc9bc975cb978f0b872fbb1781a6ea9a22f67e8a09cb54bbdc6d99d0efc081")
        file_in.close()

    def test_B3_2_full_node2(self):
        file_in = open("inputs/inputB3_2_quiz.txt","r")
        root = full_node(file_in)
        print("Merkle path node + root:", root)
        self.assertEqual(root,"Rf4582a5fe4b346a54a44fbebba114f6fcef35839f4f4cd35f5a3c801fb7e701c834bff87d2b3adaa")
        file_in.close()


if __name__ == '__main__':
    unittest.main()
