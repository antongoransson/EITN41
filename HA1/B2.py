import hashlib
from converter import *
from random import randrange
import numpy as np

def micro_mint_sim(u, k, c):
    nbr_coins = attempts = 0
    bins = [0 for x in range(2**u)]
    while (nbr_coins < c):
        x = randrange(0, 2**(2*u))
        hash_value = hash(int_to_bytes(x), u)
        bins[hash_value] += 1
        if(bins[hash_value] == k):
            nbr_coins += 1
        attempts += 1
    return attempts

def hash(x, u):
    hash_hex = hashlib.md5(x).hexdigest()
    return hex_to_int(hash_hex) % 2**u

def attempts_estimate(u = 16, k = 2, c=1, width = 22):
    lambda_interval = 3.66
    x = []
    x.append(micro_mint_sim(u, k, c))
    while(True):
        x.append(micro_mint_sim(u, k, c))
        t  = lambda_interval* np.std(x) / np.sqrt(len(x))
        if((2 * t) < width):
            break
    m = sum(x) / len(x)
    print(len(x))
    return m
