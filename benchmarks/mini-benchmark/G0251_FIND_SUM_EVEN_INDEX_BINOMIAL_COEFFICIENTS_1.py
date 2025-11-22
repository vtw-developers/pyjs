def test():
    params = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    retval_1 = 1 << (n - 1)
    return retval_1
"-----------------"
test()