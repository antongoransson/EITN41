from converter import *
import fileinput

def get_merkel_root():
    node = bytearray()
    for line in fileinput.input():
        if(fileinput.lineno() == 1):
            path = bytearray(hex_to_bytes(line[:-1]))
        else:
            node = bytearray(hex_to_bytes(line[1:-1]))
            if(line[0] == 'L'): #Decides which order the append is
                for byte in path:
                    node.append(byte)
            else:
                for byte in node:
                    path.append(byte)
                node = path
            path = bytearray(sha1_hash_bytes_array(node))
    print("Merkel root:", bytes_to_hex(sha1_hash_bytes_array(node)))


get_merkel_root()
