from functools import reduce

def threshold_scheme(k, n, f, shares, points, x = 1):
    if len(points) < k -1:
        raise Exception("Too few points on curve received")
    if len(shares) < n-1:
        raise Exception("Too few points on individual poly received")
    points[x], poly = sum(shares) + f(x), []
    for i, f in points.items():
        poly.append(f * mul_sum([j / (j - i) for j in points.keys() if i is not j]))
    return round(sum(poly))

def f(alphas):
    return lambda x: sum([alphas[i]*x**i for i in range(len(alphas))])

def mul_sum(arr):
    return reduce(lambda x, y : x * y , arr)

if __name__ == '__main__':
    k, n = 5,8
    alphas = [13, 8, 11, 1, 5]
    shares = [75, 75, 54, 52, 77, 54, 43]
    points = {2:2782, 4:30822, 5:70960, 7:256422}
    key = threshold_scheme(k, n, f(alphas), shares ,points)
    print("Key:",key)
    # Answer 110

    k, n = 4,6
    alphas = [20, 20, 11, 6]
    shares = [63, 49, 49, 54, 43]
    points = {3:2199, 4:4389, 6:12585}
    key = threshold_scheme(k, n, f(alphas), shares ,points)
    print("Key:",key)
    # Answer 93

    k, n = 5,6
    alphas = [20, 18, 13, 19, 15]
    shares = [34, 48, 45, 39, 24]
    points = {2:1908, 3:7677, 5:50751, 6:101700}
    key = threshold_scheme(k, n, f(alphas), shares ,points)
    print("Key:",key)

    k, n = 3,6
    alphas = [9, 19, 5]
    shares = [37, 18, 40, 44, 28]
    points = {4:1385, 5:2028}
    key = threshold_scheme(k, n, f(alphas), shares ,points)
    print("Key:",key)
    # Answer 53
