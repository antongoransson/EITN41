from random import randrange
from converter import *
from operator import xor

def calc_B_i(k, ID, n, e):
    B = []
    a = []
    c = []
    d = []
    r = []
    size = 30
    for i in range(2*k):
        a_i = randrange(0, 2**size)
        c_i = randrange(0, 2**size)
        d_i = randrange(0, 2**size)
        r_i = randrange(0, 2**size)

        B_i = calcul_B_i(a_i, c_i, d_i, r_i, ID, e, n)
        B.append(B_i), a.append(a_i), c.append(c_i), d.append(d_i), r.append(r_i)

    return B, a, c, d, r

def calcul_B_i(a, c, d, r, ID, e, n):
    a_i_xor  = xor(a, ID)
    # a_i_bytes = int_to_bytes(a, 4)
    c_i_bytes = int_to_bytes(c, 4)

    a_i_xor_bytes = int_to_bytes(a_i_xor, 4)
    # d_i_bytes = int_to_bytes(d, 4)
    r_i_bytes = int_to_bytes(r, 4)

    # append_arrays(a_i_bytes, c_i_bytes)
    # append_arrays(a_i_xor_bytes, d_i_bytes)
    a_i_bytes = a + c
    a_i_xor_bytes = a_i_xor + d
    x_i = sha1_hash_bytes_array(a_i_bytes)
    y_i = sha1_hash_bytes_array(a_i_xor_bytes)
    append_arrays(x_i, y_i)
    # res_i = bytes_to_int(x_i) * bytes_to_int(y_i)
    res_i = bytes_to_int(sha1_hash_bytes_array(x_i))
    B_i = ((r**e) * res_i) % n
    return B_i

def append_arrays(b1, b2):
    for b in b2:
        b1.append(b)

def recv_B(B, a, c, d, r, ID, inv, e, n):
    for i in range(0, len(B),randrange(1,3)):
        B_i = calcul_B_i(a[i], c[i], d[i], r[i], ID, e, n)
        if(B_i != B[i]):
            raise Exception("Values are not equal")
    S = 1
    B_i_1 = []
    for i in range(0, len(B), 2):
        # print("BEFORE", B[i])
        S *= (B[i]**inv)
        # print("AFTER", B[i]**inv)
    S %= n
    print("S",S)
    return S

def recv_S(S, r, n):
    x = 1
    for i in range(len(r)):
        x*=(r[i]%n)
    x = mulinv(x,n)
    print(x)
    # x = (S *x) % n
    print("X", x)
# Step 0:	26 = 1(15) + 11	p0 = 0
# Step 1:	15 = 1(11) + 4	p1 = 1
# Step 2:	11 = 2(4) + 3	p2 = 0 - 1( 1) mod 26 = 25
# Step 3:	4 = 1(3) + 1	p3 = 1 - 25( 1) mod 26 = -24 mod 26 = 2
# Step 4:	3 = 3(1) + 0	p4 = 25 - 2( 2) mod 26 = 21
#  	 	p5 = 2 - 21( 1) mod 26 = -19 mod 26 = 7
# 15 mod 26
# def extendex_euc_alg():


def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n

e = 5
n = 17*23
ID =  123456789
inv  = mulinv(e, n)
print("INV", inv)
for i in range(10):
    B, a, c, d ,r = calc_B_i(4, ID, n, e)
    S = recv_B(B, a, c, d, r, ID, inv, e, n)
    recv_S(S, r, n)
