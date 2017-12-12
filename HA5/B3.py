from base64 import b64encode
from binascii import unhexlify

def extendex_euc_alg(x, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  x, x0

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x = extendex_euc_alg(b, n)
    if g == 1:
        return x % n

def hex2(x):
    return '{}{:x}'.format('0' * (len(hex(x)) % 2), x)

def bytes_needed(i):
    if i == 0:
        return 1
    return (i.bit_length() + 7) // 8

def DER_encode_len(l):
    l_hex = hex2(l)
    if l >= 0x80:
        l_hex = '8{}{}'.format(len(l_hex) // 2, l_hex)
    return l_hex

def DER_encode_int(i):
    l = bytes_needed(i)
    i_hex = hex2(i)
    if int(i_hex[0], 16) >= 0b1000:
        i_hex = '00{}'.format(i_hex)
        l += 1
    l_hex = DER_encode_len(l)
    return '02{}{}'.format(l_hex, i_hex)

def DER_encode_cert(seq):
    l_hex = DER_encode_len(len(seq) // 2)
    return unhexlify('30{}{}'.format(l_hex, seq)) # 30 = certificate

def calc_priv_key(p, q, e, version = 0):
    n = p * q
    d = mulinv(e, (p - 1) * (q - 1))
    exp1 = d % (p - 1)
    exp2 = d % (q - 1)
    coeff = mulinv(q, p)

    priv_key = map(DER_encode_int, [version, n, e, d, p, q, exp1, exp2, coeff])
    cert = DER_encode_cert(''.join(priv_key))
    enc_cert = b64encode(cert).decode('utf8')
    key_out = ''.join(['\n' * (i % 64 == 0 and i != 0) + s for i, s in enumerate(enc_cert)])
    return enc_cert, key_out # 64 charcters per line

if __name__ == '__main__':
    p = input('p: ')
    q = input('q: ')
    e = input('e: ')
    if p == '' or q == '' or e == '':
        p = 139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763
        q = 141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
        e = 65537
        # p = 2530368937
        # q = 2612592767
    p, q, e = map(int, [p, q, e])
    b64_str, key_out = calc_priv_key(p, q, e)
    print('-----BEGIN RSA PRIVATE KEY-----\n{}\n-----END RSA PRIVATE KEY-----\n'.format(key_out))
