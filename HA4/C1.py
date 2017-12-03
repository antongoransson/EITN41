from hashlib import sha1
from random import randrange
from sys import argv
from helpers import *
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("eitn41.eit.lth.se", 1337))

def recv():
    return soc.recv(4096).decode('utf8').strip()

def otr_smp(passphrase, p, g, g1, msg):
    p = h_int(p)
    ##########################
    #### D-H Key Exchange ####
    ##########################
    g_x1 = h_int(recv())

    x2 = randrange(2, p)
    g_x2 = pow(g, x2, p)
    g_x2_str = h_str(g_x2)
    soc.send(encode(g_x2_str))
    print ('\nsent g_x2:', recv())

    DH_key = byte(pow(g_x1, x2, p))

    ##########################
    ########## SMP ###########
    ##########################
    g2_a = h_int(recv())
    print ('\nreceived g_2a')

    b2 = randrange(2, p)
    g1_b2 = pow(g1, b2, p)
    g1_b2_str = h_str(g1_b2)
    soc.send(encode(g1_b2_str))
    print ('\nsent g1_b2:', recv())

    g3_a = h_int(recv())
    print ('\nreceived g3_a')

    b3 = randrange(2, p)
    g1_b3 = pow(g1, b3, p)
    g1_b3_str = h_str(g1_b3)

    soc.send(encode(g1_b3_str))
    print ('\nsent g1_b3:', recv())

    P_a = h_int(recv())
    print ('\nreceived P_a')

    b = randrange(2, p)
    g3 = pow(g3_a, b3, p)

    P_b = pow(g3, b, p)
    P_b_str = h_str(P_b)
    soc.send(encode(P_b_str))
    print ('\nsent P_B:', recv())

    Q_a = h_int(recv())
    print ('\nreceived Q_a')
    g2 = pow(g2_a, b2, p)

    y = b_int(sha1(DH_key + passphrase).digest())

    Q_b = pow(g1, b, p) * pow(g2, y, p)
    Q_b_str = h_str(Q_b)
    soc.send(encode(Q_b_str))
    print ('\nsent Q_b:', recv())

    R_a = h_int(recv())
    print ('\nreceived R_a')

    Q_b_inv = mulinv(Q_b, p)

    R_b = pow(Q_a * Q_b_inv, b3, p)
    R_b_str = h_str(R_b)
    soc.send(encode(R_b_str))
    print ('\nsent R_b:', recv())

    print ('\nAuthenticated', recv())

    R_ab = pow(R_a, b3, p)
    P_b_inv = mulinv(P_b, p)
    print("ACK", R_ab == P_a * P_b_inv % p)

    msg = byte(0, size = 1) * (len(DH_key) - len(h_bytes(msg))) + h_bytes(msg)

    enc_msg = bytes(a ^ b for a, b in zip(msg, DH_key))
    enc_msg_str = h_str(b_int(enc_msg))

    soc.send(encode(enc_msg_str))
    return recv()

if __name__ == '__main__':
    if len(argv) == 2:
        msg = argv[1]
    else:
        msg = "66a17e82a5bd6de67aeace5e64c3fe3a831a50d6"
    passphrase = encode("eitn41 <3")
    g = g1 = 2
    p = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF"
    encr_msg = otr_smp(passphrase, p, g, g1, msg)
    print(encr_msg)
