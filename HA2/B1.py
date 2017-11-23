def dc_broadcast(SA, SB, DA, DB, m, b):
    if(b == 1):
        BC = int(DA, 16) ^ int(DB, 16) ^ int(m, 16)
        BC = hex(BC)[2:].zfill(4)
    else:
        D = int(SA, 16) ^ int(SB, 16)
        BC = hex(D)[2:].zfill(4) + hex(int(DA, 16) ^ int(DB, 16) ^ D)[2:].zfill(4)
    return BC.upper()

if __name__ == '__main__':
    SA = '0000'
    DA = '7490'
    SB = '0010'
    DB = 'F29D'
    M = '0DBB'
    b = 0
    broadcast = dc_broadcast(SA, SB, DA, DB, M, b)
    print("Broadcast:", broadcast)
