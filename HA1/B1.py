import fileinput

def find_value_x(card_nbr):
    list_nbrs = list(reversed(card_nbr))
    nbr_sum, index = calc_sum(list_nbrs)
    value = (10 - (nbr_sum % 10)) % 10
    if((index + 1) % 2 == 0 ):
        if(value % 2 != 0):
            value += 9
        value /= 2
    return str(round(value))

def calc_sum(card_nbr):
    tot_sum = 0
    index = 0
    for i in range(0, len(card_nbr)):
        if(card_nbr[i] == 'X'):
            index = i
            continue
        nbr = int(card_nbr[i])
        if((i + 1) % 2 == 0):
            nbr *= 2
            if(nbr >= 10):
                nbr -= 9
        tot_sum += nbr
    return tot_sum, index

def get_values_from_file(file_in):
    string = ""
    for line in file_in:
        string += find_value_x(line[:-1])
    return string


if __name__ == "__main__":
    string = ""
    for line in fileinput.input():
        string += find_value_x(line[:-1])
    print(string)
