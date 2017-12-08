from converter import *
from random import randrange
import matplotlib.pyplot as plt

def new_commit(X):
    v = randrange(0, 2)
    rand = randrange(0, 2**16)
    return v, commitment_scheme(v, rand, X)

#Binding – Sender can not change her mind after committing to the value==
# Sender finding new hash for v != v:_start
#Concealing – Receiver can not determine value of v before revealing
# Reciver finding the value commited by sender
def commitment_scheme(v, k, X):
    v_k = int_to_bytes(v, size=1) + int_to_bytes(k, size=2)
    return bytes_to_int(sha1_hash(v_k)) % 2**X

def binding_probability(X):
    v, s_commit = new_commit(X)
    v_new = 1 ^ v
    for i in range(2**16):
        commit = commitment_scheme(v_new, i, X)
        if commit == s_commit:
            return 1
    return 0

def conceal_probability(X):
    v0, v1 = 0, 1
    v, s_commit = new_commit(X)
    commits = {0: [], 1: []}
    for i in range(2**16):
        c0 = commitment_scheme(v0, i, X)
        c1 = commitment_scheme(v1, i, X)
        if c0 == s_commit: commits[v0].append(c0)
        if c1 == s_commit: commits[v1].append(c1)
    return len(commits[v]) / (len(commits[v0]) + len(commits[v1]))

if __name__ == '__main__':
    conceal_prob_tot, binding_prob_tot = [], []
    start, end, step, res = 0, 30, 1, 5
    for X in range(start, end, step):
        binding_prob = [binding_probability(X) for k in range(res)]
        conceal_prob = [conceal_probability(X) for k in range(res)]
        binding_prob_tot.append(100*(sum(binding_prob) / len(binding_prob)))
        conceal_prob_tot.append(100*(sum(conceal_prob) / len(conceal_prob)))
        print(round(100 * X / (end - start )),"%")
    x = [X for X in range(start, end, step)]
    plt.plot(x, binding_prob_tot, label="Binding prob")
    plt.plot(x, conceal_prob_tot, label="Conceal prob")
    plt.ylabel('Prob of breaking scheme in %')
    plt.xlabel('Nbr of bits used of hash')
    plt.legend(loc='best')
    plt.show()
