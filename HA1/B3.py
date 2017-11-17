from converter import *
import fileinput
from math import log2, ceil

def get_merkle_root(file_in):
    if file_in is None:
        raise Exception("A filed needs to be provided")
    left, right, node_list = read_file_B3_1(file_in)
    return get_merkle_root_rec(left, right, node_list)

def get_merkle_root_rec(left, right, node_list):
    left, right = hex_to_bytes(left), hex_to_bytes(right)
    for byte in right:
        left.append(byte)
    path = bytes_to_hex(sha1_hash(left))
    if len(node_list) == 0:
        return path
    nextNode = node_list.pop(0)
    if nextNode[0] == 'L': #Decides which order the append is
        return get_merkle_root_rec(nextNode[1:], path, node_list)
    else:
        return get_merkle_root_rec(path, nextNode[1:], node_list)

def build_merkle_tree(nodes, parents):
    if(len(parents) == 1):
        return nodes
    x = []
    for i in range(0, len(parents), 2):
        h1, h2 = bytearray(parents[i]), parents[i + 1]
        for byte in h2:
            h1.append(byte)
        parent = sha1_hash(h1)
        nodes.append(parent), x.append(parent)
    if len(x) != 1 and len(x) % 2 != 0:
        nodes.append(x[-1]), x.append(x[-1])
    return build_merkle_tree(nodes, x)

def find_nodes_per_depth(nbr_of_leaves, depth):
    nodes_per_depth = [nbr_of_leaves]
    for i in range(1, depth + 1):
        nbr_nodes = nodes_per_depth[i-1] // 2
        if(nbr_nodes != 1 and nbr_nodes % 2 != 0):
            nbr_nodes += 1
        nodes_per_depth.append(nbr_nodes)
    return nodes_per_depth

def build_merkle_path(nodes, i, j, depth, nbr_of_leaves):
    path, parentindex, first_node_index = [], i, 0
    nodes_per_depth = find_nodes_per_depth(nbr_of_leaves, depth)
    for k in range(depth):
        curr_index = parentindex + first_node_index
        if curr_index % 2 == 0:
            node = "R" + bytes_to_hex(nodes[curr_index + 1])
        else:
            node = "L" + bytes_to_hex(nodes[curr_index - 1])
        path.append(node)
        parentindex = (curr_index - first_node_index) // 2
        first_node_index += nodes_per_depth[k]
    return list(reversed(path))

def read_file_B3_1(file_in):
    left, right = file_in.readline()[:-1], file_in.readline()[1:-1]
    node_list = [line[:-1] for line in file_in]
    return left, right, node_list

def read_file_B3_2(file_in):
    i, j = file_in.readline()[:-1], file_in.readline()[:-1]
    leaves = [hex_to_bytes(line[:-1]) for line in file_in]
    return int(i), int(j), leaves

def full_node(file_in):
    if file_in is None:
        raise Exception("A file needs to be provided")
    i, j, leaves = read_file_B3_2(file_in)
    nbr_of_leaves = len(leaves)
    depth, tree = ceil(log2(nbr_of_leaves)), leaves
    tree = build_merkle_tree(tree, leaves)
    path = build_merkle_path(tree, i, j, depth, nbr_of_leaves)
    return path[j-1]+ bytes_to_hex(tree[-1])

if __name__ == '__main__':
    input_var = input("Please choose task (1 or 2):")
    if(str(input_var) == "1"):
        print(get_merkle_root(fileinput.input()))
    elif(str(input_var) == "2"):
        print(full_node(fileinput.input()))
