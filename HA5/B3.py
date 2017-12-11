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

def TLV_DER_INT(i):
    l = bytes_needed(i)
    i_str = hex2(i)
    if int(i_str[0], 16) >= 0b1000: #1000 or larger
        i_str = '00' + i_str
        l += 1
    l_str = hex2(l)
    if l > 0x7f:
        l_str = '8' + str(len(l_str) // 2) + l_str
    return '02' + l_str + i_str

def TLV_DER_CERT(seq):
    l = hex2(len(seq) // 2 )
    if len(seq) // 2 > 0x7f:
        l = '8' + str(len(l) // 2) + l
    return unhexlify('30' + l + seq) # 30 = certificate

def calc_priv_key(p, q, e, version = 0):
    n = p * q
    d = mulinv(e, (p - 1) * (q - 1))
    exp1 = d % (p - 1)
    exp2 = d % (q - 1)
    coeff = mulinv(q, p)

    priv_key = map(TLV_DER_INT, [version, n, e, d, p, q, exp1, exp2, coeff])
    cert = TLV_DER_CERT(''.join(priv_key))
    key_out = b64encode(cert).decode('utf8')
    key_out= ''.join(['\n' *( i % 64 == 0 and i != 0) + s for i, s in enumerate(key_out)])
    return b64encode(cert).decode('utf8'), key_out# 64 charcters per line

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
