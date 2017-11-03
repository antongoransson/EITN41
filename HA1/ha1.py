import sys
sys.path.insert(0, '/home/anton/Git/EITN41/helpers/')
from converter import * #



def find_x_value(card_nbr):
    for i in range(len(str(card_nbr))-1, 0, -1):
        if(card_nbr[i] == 'X'):
            return i

def calc_checksum(card_nbr):
    card_nbr_list = list(card_nbr)
    for i in range(len(card_nbr_list)-1, 0, -1):
        nbr = int(card_nbr_list[i])
        if((i+1) % 2 == 0):
            card_nbr_list[i] = str(2 * nbr)
        if(int(card_nbr_list[i]) > 10):
            card_nbr_list[i] = str(1 + int(card_nbr_list[i]) % 10)
    checksum = 0
    for i in card_nbr_list:
        checksum+=int(i)

    print(checksum)
    print(checksum % 10 )
print(int_to_hex(5))
print(find_x_value("12314X"))
calc_checksum(str(79927398710))
