from random import randrange, sample
from converter import *
import operator
import functools


def calc_B_i(k, ID, n, e, inv, size = 2**20):
    B,quadruples, a, c, d, r  = [[0 for i in range(2*k)] for i in range(6)]
    B_TEST = []
    for i in range(2 * k):
        a_i, c_i, d_i, r_i= [randrange(1, size) for x in range(4)]
        B_i = calcul_B_i(a_i, c_i, d_i, r_i, ID, e, n, B_TEST)
        B[i] = B_i
        quadruples[i] = a_i, c_i, d_i ,r_i
    return B, B_TEST, quadruples

def calcul_B_i(a, c, d, r, ID, e, n, B_TEST = None):
    x_i = sha1_hash(a + c)
    y_i = sha1_hash(a ^ ID + d)
    f_x_y = bytes_to_int(x_i) * bytes_to_int(y_i)

    if B_TEST is not None:
        B_TEST.append(f_x_y)
    B_i = r**e * f_x_y % n

    return B_i

def receive_signature(B, ID, inv, e, n, k, R, quadruples):
    for i in R:
        a, c, d, r = quadruples[i]
        B_i = calcul_B_i(a, c, d, r, ID, e, n)
        if(B_i != B[i]):
            raise Exception("Values are not equal")
    S = 1
    R_I = [i for i in range(len(B)) if i not in R]
    # functools.reduce(lambda:, [1,2,3,4,5,6], 1)
    for i in R_I:
        S *= pow(B[i], inv, n)
    S = S % n
    print("Bank",S)
    return S, R_I

def calc_S(S, quadruples_R_I, n, d, R_I):
    x = 1
    for i in R_I:
        _, _, _, r = quadruples_R_I[i]
        x *= r
    x = (S * mulinv(x, n)) % n
    print("Alice", x)
    return x

def getIndices(B):
    return sorted(sample(range(len(B)), len(B) // 2))

def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  x, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = extendex_euc_alg(b, n)
    if g == 1:
        return x % n

def totient(p, q):
    return (p - 1) * (q - 1)

p = 1033
q = 1299721
e = 17
n = (p) * (q) # 127*89= 11303
totient_n = totient(p, q)
ID =  1234415161711
k = 4
priv_key  = mulinv(e, totient_n)
# print("INV", priv_key)
for i in range(10):
    B, B_TEST, quadruples = calc_B_i(k, ID, n, e , priv_key) # STEP 1
    R = getIndices(B) # STEP 2
    quadruples_R = { i: quadruples[i] for i in R}
    sign, R_I = receive_signature(B, ID, priv_key, e, n, k, R, quadruples_R) #STEP 3.2
    quadruples_R_I = { i: quadruples[i] for i in R_I}
    x = 1
    y = 1
    for i in R_I:
        x *= pow(B_TEST[i], priv_key, n)
    for i in R_I:
        y *= B_TEST[i]
    x = x % n
    S = calc_S(sign, quadruples_R_I, n, priv_key, R_I)
    print(S == x)
    print(y % n)
    print(pow(S, e, n))
