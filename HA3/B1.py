from converter import *
import os
import numpy as np
import scipy as sp
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t.ppf(( 1+ confidence) / 2., n-1)
    return m, m-h, m+h

#Binding – Sender can not change her mind after committing to the value
#Concealing – Receiver can not determine value of v before revealing
def commitment_scheme(v, k, X):
    a = bytearray(int_to_bytes(v, size = 1))
    a.append(k)
    return bytes_to_int(sha1_hash(a)) % 2**X

def binding_probability(X):
    v_start, v_break = 0, 1
    start_k = os.urandom(1)[0]
    commit = commitment_scheme(v_start, start_k, X)
    mean_tries, k_arr  = [], []
    for i in range(1000):
        tries = 0
        k = os.urandom(1)[0]
        a = commitment_scheme(v_break, k, X)
        while commit != a:
            tries += 1
            k = os.urandom(1)[0]
            a = commitment_scheme(v_break, k, X)
        k_arr.append(k)
        mean_tries.append(tries)
    # print(mean_confidence_interval(mean_tries))
    print(len(mean_tries) / sum(mean_tries))
    print(
    "k_start", start_k, int_to_hex(commitment_scheme(v_start, start_k, X)),
    "BROKEN", int_to_hex(commitment_scheme(v_break, k_arr[0], X)), "K",k_arr[0]
    )
    # print(
    # "k_start", start_k, (commitment_scheme(v_start, start_k, X)),
    # "BROKEN", (commitment_scheme(v_break, k_arr[0], X)), "K",k_arr[0]
    # )
    print("BINDING",(len(mean_tries) / sum(mean_tries))* 100 ,'%')
    print("X =",X)

def concealing_probability(X):

    h = commitment_scheme(1, os.urandom(1)[0], X)
    mean_tries = []
    for i in range(100000):
        tries = 0
        while h !=commitment_scheme(1, os.urandom(1)[0], X):
            tries += 1
        mean_tries.append(tries)
    print(mean_confidence_interval(mean_tries))
    # print(len(mean_tries) / sum(mean_tries))
    print("CONCEALING", (len(mean_tries) / sum(mean_tries))* 100 ,'%')
    print(mean_confidence_interval(mean_tries))

X = 10

binding_probability(X)
