from converter import *
import os
from random import randrange
import numpy as np
import scipy as sp
import scipy.stats
import random

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t.ppf(( 1+ confidence) / 2., n-1)
    return m, m-h, m+h

#Binding – Sender can not change her mind after committing to the value==
# Sender finding new hash for v != v:_start
#Concealing – Receiver can not determine value of v before revealing
# Reciver finding the value commited by sender
def commitment_scheme(v, k, X):
    v = bytes_to_hex(int_to_bytes(v, size=1))
    k = bytes_to_hex(int_to_bytes(k, size=2))
    return bytes_to_int(sha1_hash(hex_to_bytes(v+k))) % 2**X

def binding_probability(s_commit, v, X):
    v_new = 1 if v == 0 else 0
    commits = {v_new: []}
    found = False
    for i in range(2**16):
        commit = commitment_scheme(v_new, i, X)
        if commit == s_commit:
            found = True
            break
    return 1 if found else 0

def concealing_probability(s_commit, X):
    commits = {0: [], 1: []}
    for v in range(2):
        for i in range(2**16):
            commit = commitment_scheme(v, i, X)
            if commit == s_commit:
                commits[v].append(commit)
    possibilites = len(commits[0]) + len(commits[1])
    # print("Nbr of probable values: {}".format(possibilites))
    # print("Probability of find correct one: {}%".format(100*(1 / possibilites)))
    return 1 / possibilites

conceal_prob,binding_prob = [], []
for X in range(100):
    v = randrange(0, 2)
    X = 16 # X > 25 100%
    rand = randrange(0, 2**16)
    s_commit = commitment_scheme(v, rand, X)
    binding_prob.append(binding_probability(s_commit, v, X))
    conceal_prob.append(concealing_probability(s_commit, X))
print("Breaking binding property prob", 100*(sum(binding_prob)/ len(binding_prob)),"%")
print("Breaking concealing property prob", 100*(sum(conceal_prob)/ len(conceal_prob)),"%")
