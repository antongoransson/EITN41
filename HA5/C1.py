from hashlib import sha1
from random import randrange
from sys import argv

def h_int(h):
  return int(h, 16)

def b_int(b):
  return int.from_bytes(b, byteorder='big')

def jacobi (a, m):
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
  return  x, x0, y0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
  g, x, _ = extendex_euc_alg(b, n)
  if g == 1:
      return x % n

def PKG(a, M, p, q):
  return pow(a, (M + 5 - p - q) // 8, m)

def find_a(identity, m):
  h = sha1(identity.encode('utf8'))
  while jacobi(b_int(h.digest()), m) != 1:
    h = sha1(h.digest())
  return h.hexdigest()

def find_t(m):
  t = randrange(0, m)
  while jacobi(t, m) != 1:
    t = randrange(0, m)
  return t

def find_bit(bits, r, m):
  b = [jacobi(h_int(s) + 2 * r, m) for s in bits]
  b = [x + 1 if x < 0 else x for x in b]
  return int(''.join(map(str, b)), 2)

if __name__ == '__main__':
  identity = 'walterwhite@crypto.sec'
  p = h_int('9240633d434a8b71a013b5b00513323f')
  q = h_int('f870cfcd47e6d5a0598fc1eb7e999d1b')
  m = p  * q
  encrypted_bits = []
  while True:
    try: encrypted_bits.append((input('')))
    except: break
  a = h_int(find_a(identity, m))
  r = PKG(a, m, p, q)
  t = find_t(m)
  s = (t + a * mulinv(t, m)) % m
  code = find_bit(encrypted_bits, r, m)
  print('r:', hex(r)[2:])
  print('CODE:', code)
