from hashlib import sha1
from random import randrange
from sys import argv
from binascii import unhexlify
import socket



def I2OSP(x, xLen):
    X = []
    for i in range(xLen):
        X.append(x % 256)
        x //= 256
    return bytes(X[::-1])

def byte(x, size=None):
    if size is None:
        size = (x.bit_length() + 7) // 8
    return x.to_bytes(size, 'big')

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

def recv():
    return soc.recv(4096).decode('utf8').strip()

def send(x):
    soc.send(format(x, 'x').encode('utf8'))

def recv_int():
    return int(soc.recv(4096).decode('utf8').strip(), 16)

def otr_smp(passphrase, p, g, g1, msg):
    p = int(p, 16)

    ##########################
    #### D-H Key Exchange ####
    ##########################
    g_x1 = recv_int()

    x2 = randrange(2, p)
    g_x2 = pow(g, x2, p)
    send(g_x2)
    print ('\nsent g_x2:', recv())

    DH_key = byte(pow(g_x1, x2, p))

    ##########################
    ########## SMP ###########
    ##########################
    g2_a = recv_int()
    print ('\nreceived g_2a')

    b2 = randrange(2, p)
    g1_b2 = pow(g1, b2, p)
    send(g1_b2)
    print ('\nsent g1_b2:', recv())

    g3_a = (recv_int())
    print ('\nreceived g3_a')

    b3 = randrange(2, p)
    g1_b3 = pow(g1, b3, p)
    send(g1_b3)
    print ('\nsent g1_b3:', recv())

    P_a = recv_int()
    print ('\nreceived P_a')

    b = randrange(2, p)
    g3 = pow(g3_a, b3, p)

    P_b = pow(g3, b, p)
    send(P_b)
    print ('\nsent P_B:', recv())

    Q_a = recv_int()
    print ('\nreceived Q_a')
    g2 = pow(g2_a, b2, p)

    y = int(sha1(DH_key + passphrase).hexdigest(), 16)

    Q_b = pow(g1, b, p) * pow(g2, y, p)
    send(Q_b)
    print ('\nsent Q_b:', recv())

    R_a = recv_int()
    print ('\nreceived R_a')

    Q_b_inv = mulinv(Q_b, p)

    R_b = pow(Q_a * Q_b_inv, b3, p)
    send(R_b)
    print ('\nsent R_b:', recv())

    print ('\nAuthenticated', recv())

    R_ab = pow(R_a, b3, p)
    P_b_inv = mulinv(P_b, p)
    print("ACK", R_ab == P_a * P_b_inv % p)

    msg = I2OSP(0, len(DH_key) - len(msg) // 2)  + unhexlify(msg)
    enc_msg = bytes(a ^ b for a, b in zip(msg, DH_key))
    send(int.from_bytes(enc_msg, byteorder='big'))

    return recv()

if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("eitn41.eit.lth.se", 1337))
    if len(argv) == 2:
        msg = argv[1]
    else:
        msg = "66a17e82a5bd6de67aeace5e64c3fe3a831a50d6"
    passphrase = "eitn41 <3".encode('utf8')
    g = g1 = 2
    p = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF"
    encr_msg = otr_smp(passphrase, p, g, g1, msg)
    print(encr_msg)
