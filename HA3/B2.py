from functools import reduce

def threshold_scheme(k, n, f_1, s, f, x = 1):
    f[x] = sum(s) + f_1(x)
    poly = [f[i] * mul_sum([j / (j - i) for j in f if i is not j]) for i in f]
    return round(sum(poly))

def f_x(a):
    return lambda x: sum([a[i]*x**i for i in range(len(a))])

def mul_sum(arr):
    return reduce(lambda x, y : x * y , arr)

if __name__ == '__main__':
    k, n = 5,8
    a = [13, 8, 11, 1, 5]
    s = [75, 75, 54, 52, 77, 54, 43]
    f = {2:2782, 4:30822, 5:70960, 7:256422}
    key = threshold_scheme(k, n, f_x(a), s ,f)
    print("Key:",key)
    # Answer 110

    k, n = 4,6
    a = [20, 20, 11, 6]
    s = [63, 49, 49, 54, 43]
    f = {3:2199, 4:4389, 6:12585}
    key = threshold_scheme(k, n, f_x(a), s ,f)
    print("Key:",key)
    # Answer 93

    k, n = 5,6
    a = [20, 18, 13, 19, 15]
    s = [34, 48, 45, 39, 24]
    f = {2:1908, 3:7677, 5:50751, 6:101700}
    key = threshold_scheme(k, n, f_x(a), s ,f)
    print("Key:",key)

    k, n = 3,6
    a = [9, 19, 5]
    s = [37, 18, 40, 44, 28]
    f = {4:1385, 5:2028}
    key = threshold_scheme(k, n, f_x(a), s ,f)
    print("Key:",key)
    # Answer 53
