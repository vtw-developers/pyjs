def test():
    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    if n == 2 or n == 3:
        return n - 1
    res = 1
    while n > 4:
        n -= 3
        res *= 3
    ret_val = n * res
    return ret_val
"-----------------"
test()