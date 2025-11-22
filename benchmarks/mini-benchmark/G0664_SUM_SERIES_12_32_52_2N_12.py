def test():
    params = [14, 61, 37, 86, 47, 98, 70, 24, 76, 24]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sum_0 = 0
    for i in range(1, n + 1):
        sum_0 = sum_0 + (2 * i - 1) * (2 * i - 1)
    return sum_0
"-----------------"
test()