from binascii import unhexlify, hexlify

def h_bytes(h):
    return bytearray(unhexlify(h)) # converts string to byte_array

def b_to_h(b):
    return hexlify(b).decode('utf-8')

def h_str(x):
    return format(x, 'x')

def byte(x, size=None):
    if size is None:
        size = (x.bit_length() + 7) // 8
    return x.to_bytes(size, 'big')

def h_int(h):
    return int(h, 16)

def b_int(b):
    return int.from_bytes(b, byteorder='big')


def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  x, x0, y0

def encode(s):
    return s.encode('utf8')
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = extendex_euc_alg(b, n)
    if g == 1:
        return x % n
