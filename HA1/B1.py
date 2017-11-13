import fileinput

def find_value_x(card_nbr):
    list_nbrs = list(reversed(card_nbr))
    nbr_sum, index = calc_sum(list_nbrs)
    value = (10 - (nbr_sum % 10)) % 10
    if((index + 1) % 2 == 0 ):
        if(value % 2 != 0):
            value += 9
        value //= 2
    return str((value))

def calc_sum(card_nbr):
    tot_sum = index = 0
    for i in range(len(card_nbr)):
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
    if file_in is None:
        raise Exception("A filed needs to be provided")
    string = ""
    for line in file_in:
        string += find_value_x(line[:-1])
    return string


if __name__ == "__main__":
    string = get_values_from_file(fileinput.input())
    print(string)
