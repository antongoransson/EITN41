from converter import *
import fileinput
from math import log2, ceil

def get_merkle_root(file_in):
    node_list = []
    left = file_in.readline()[:-1]
    right = file_in.readline()[1:-1]
    for line in file_in:
        node_list.append((line[:-1]))
    return get_merkle_root_rec(left, right, node_list)

def get_merkle_root_rec(left, right, node_list):
    left = hex_to_bytes(left)
    right = hex_to_bytes(right)
    for byte in right:
        left.append(byte)
    if(len(node_list) == 0):
        return  bytes_to_hex(sha1_hash_bytes_array(left))
    nextNode = node_list.pop(0)
    if(nextNode[0] == 'L'): #Decides which order the append is
        return get_merkle_root_rec(nextNode[1:], bytes_to_hex(sha1_hash_bytes_array(left)), node_list)
    else:
        return get_merkle_root_rec(bytes_to_hex(sha1_hash_bytes_array(left)), nextNode[1:], node_list)

def build_merkle_tree(nodes, parents):
    if(len(parents) == 1):
        return
    x = []
    for i in range(0, len(parents), 2):
        h1 = bytearray(parents[i])
        h2 = parents[i+1]
        for byte in h2:
            h1.append(byte)
        parent = sha1_hash_bytes_array(h1)
        nodes.append(parent)
        x.append(parent)
    if(len(x) != 1 and len(x) % 2 != 0):
        nodes.append(x[-1])
        x.append(x[-1])
    build_merkle_tree(nodes, x)

def find_nodes_per_depth(nbr_of_leaves, depth):
    nodes_per_depth = [nbr_of_leaves]
    for i in range(1, depth + 1):
        nbr_nodes = nodes_per_depth[i-1] / 2
        if(nbr_nodes != 1 and nbr_nodes % 2 != 0):
            nbr_nodes+=1
        nodes_per_depth.append(nbr_nodes)
    return nodes_per_depth

def build_merkle_path(nodes, i , j, depth, nbr_of_leaves):
    path = []
    parentindex =  curr_index = i
    nodes_per_depth = find_nodes_per_depth(nbr_of_leaves, depth)
    first_node_index = 0
    for k in range(depth):
        curr_index = int(parentindex + first_node_index)
        if(curr_index % 2 == 0):
            node = "R" + bytes_to_hex(nodes[curr_index + 1])
        else:
            node = "L" + bytes_to_hex(nodes[curr_index - 1])
        path.append(node)
        parentindex = int((curr_index - first_node_index) / 2)
        first_node_index += nodes_per_depth[k]
    return list(reversed(path))

def read_file(file_in):
    leaves = []
    i = file_in.readline()[:-1]
    j = file_in.readline()[:-1]
    for line in file_in:
        leaves.append(hex_to_bytes(line[:-1]))
    return int(i), int(j), leaves

def full_node(file_in):
    if file_in is None:
        raise Exception("A filed needs to be provided")
    i, j , leaves = read_file(file_in)
    depth = ceil(log2(len(leaves)))
    tree = leaves
    nbr_ofleaves = len(leaves)
    build_merkle_tree(tree, leaves)
    path = build_merkle_path(tree, i, j, depth, nbr_ofleaves)
    return path[j-1]+ bytes_to_hex(tree[-1])

if __name__ == '__main__':
#     input_var = input("Please choose task (T1 or T2):")
#     if(str(input_var) == "T1"):
#         get_merkle_root()
#     elif(str(input_var)== "T2"):
    print(full_node(fileinput.input()))
