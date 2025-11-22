def test():
    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    res = 1
    for i in range(n, -1, -2):
        if i == 0 or i == 1:
            return res
        else:
            res *= i
    return res
"-----------------"
test()