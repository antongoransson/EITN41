import fileinput

def find_value_x(card_nbr):
    list_nbr= list(reversed(card_nbr))
    index = find_index_x(list_nbr)
    nbr_sum = calc_sum(list_nbr)
    value = 10 - (nbr_sum % 10)
    if(value == 10):
        value = 0
    if((index + 1) % 2 == 0 ):
        if((value + 9) % 2 == 0):
            value+=9
        value/=2
    return int(value)

def find_index_x(card_nbr):
    for i in range(0, len((card_nbr))):
        if(card_nbr[i] == 'X'):
            return i

def calc_sum(card_nbr):
    tot_sum = 0
    for i in range(0, len(card_nbr)):
        if(card_nbr[i] == 'X'):
            continue
        nbr = int(card_nbr[i])
        if((i + 1) % 2 == 0):
            nbr *= 2
            if(nbr >= 10):
                nbr -= 9
        tot_sum += nbr
    return tot_sum

string = ""
for line in fileinput.input():
    string+=(str(find_value_x(str(line)[:-1])))
print(string)
