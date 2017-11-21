from functools import reduce
from sys import argv

# Least common multiple is not in standard libraries? It's in gmpy, but this is simple enough:
def L_func(n):
    return lambda x: (x - 1) / n

def totient(p, q):
    return (p - 1) * (q - 1)
# Taken from
#https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  x, x0, y0

def mul_sum(arr):
    return reduce(lambda x, y : x * y , arr)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = extendex_euc_alg(b, n)
    if g == 1:
        return x % n

if __name__ == '__main__':
    if len(argv) > 1 and argv[1] == "f":
        print("Read from file")
        votes = []
        while True:
            try:
                votes.append(input(''))
            except EOFError:
                break
        votes = [int(line) for line in votes]
        p, q, g = 1117, 1471, 652534095028
    else:
        votes = [929, 296, 428]
        p, q, g = 5, 7, 867
    prod_sum = mul_sum(votes)
    n = p * q
    L = L_func(n)
    l = totient(p,q)
    my = mulinv(L(pow(g, l, n**2)), n)
    prod = pow(prod_sum,l, n**2)
    vote_sum = L(prod) * my % n
    if vote_sum > len(votes):
        print(vote_sum - n)
    else:
        print(vote_sum)
