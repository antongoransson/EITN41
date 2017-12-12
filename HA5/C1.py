from hashlib import sha1
from random import randrange
from sys import argv

def b_int(b):
    return int.from_bytes(b, byteorder='big')

def jacobi(a, m):
    j = 1
    a %= m
    while a:
        t = 0
        while not a & 1:
            a = a >> 1
            t += 1
        if t & 1 and m % 8 in (3, 5):
            j = -j
        if (a % 4 == m % 4 == 3):
            j = -j
        a, m = m % a, a
    return j if m == 1 else 0

def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = extendex_euc_alg(b, n)
    if g == 1:
        return x % n

def PKG(a, m, p, q):
    return pow(a, (m + 5 - p - q) // 8, m)

def quadratic_residue(identity, m):
    a = sha1(identity.encode('utf8')).digest()
    while jacobi(b_int(a), m) != 1:
        a = sha1(a).digest()
    return b_int(a)

def get_t(m):
    t = randrange(0, m)
    while jacobi(t, m) != 1:
        t = randrange(0, m)
    return t

def decrypt_bits(encrypted_bits, r, m):
    b = [jacobi(int(s, 16) + 2 * r, m) for s in encrypted_bits]
    b = [0 if x < 0 else x for x in b]
    return int(''.join(map(str, b)), 2)

def IBE(identity, p, q, encrypted_bits):
    m = p * q
    a = quadratic_residue(identity, m)
    r = PKG(a, m, p, q)
    t = get_t(m)
    s = (t + a * mulinv(t, m)) % m
    code = decrypt_bits(encrypted_bits, r, m)
    print('r:', format(r, 'x'))
    print('CODE:', code)


if __name__ == '__main__':
    identity = input('')
    p, q = int(input(''), 16), int(input(''), 16)
    encrypted_bits = []
    while True:
        try: encrypted_bits.append((input('')))
        except: break
    IBE(identity, p, q, encrypted_bits)
