from random import randrange, sample
from converter import *
from functools import reduce


def calculate_B(k, ID, n, e, inv, size = 2**20):
    B, quadruples = [[0 for i in range(2*k)] for i in range(2)]
    f_x_y = []
    for i in range(2 * k):
        a_i, c_i, d_i, r_i = [randrange(1, size) for x in range(4)]
        B[i] = calculate_B_i(a_i, c_i, d_i, r_i, ID, e, n, f_x_y)
        quadruples[i] = a_i, c_i, d_i, r_i
    return B, quadruples, f_x_y

def calculate_B_i(a, c, d, r, ID, e, n, f = None):
    x_i = sha1_hash(a + c)
    y_i = sha1_hash(a ^ ID + d)
    f_x_y = bytes_to_int(x_i) * bytes_to_int(y_i)

    if f is not None:
        f.append(f_x_y)
    B_i = r**e * f_x_y % n
    return B_i

def receive_signature(B, ID, priv_key, e, n, R, quadruples):
    for i in R:
        a, c, d, r = quadruples[i]
        B_i = calculate_B_i(a, c, d, r, ID, e, n)
        if(B_i != B[i]):
            raise Exception("Values are not equal")
    R_sign = [i for i in range(len(B)) if i not in R]
    B_to_sign = [B[i] for i in R_sign]
    signed_B = pow(reduce(lambda x, y : x * y %n, B_to_sign), priv_key, n)
    return signed_B, R_sign

def calc_S(signed_B, quadruples, n, R_sign):
    r = [quadruples[i][3] for i in R_sign]
    S = signed_B * mulinv(reduce(lambda x, y : x * y , r), n) % n
    return S

# Taken from
#https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
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

p, q, e = 1300097, 1299721, 17
n = p * q # 127*89= 11303
totient_n = totient(p, q)
ID =  1251261711
k = 100
priv_key  = mulinv(e, totient_n)
# print("INV", priv_key)
for i in range(1000):
    B, quadruples, f_x_y = calculate_B(k, ID, n, e, priv_key) # STEP 1
    R = sample(range(len(B)), len(B) // 2) # STEP 2
    quadruples_R = {i: quadruples[i] for i in R}
    signed_B, R_sign = receive_signature(B, ID, priv_key, e, n, R, quadruples_R) #STEP 3.2

    f_sign = [f_x_y[i] for i in R_sign]
    prod_sum_f = reduce(lambda x, y: x * y, f_sign)
    x = pow(prod_sum_f, priv_key, n)

    S = calc_S(signed_B, quadruples, n, R_sign)
    print("SIGNED VALUE OK", S == x)
    print("SIGNATURE OK", prod_sum_f % n == pow(S, e, n))
    # print(S)
