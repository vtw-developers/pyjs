def test():
    params = [67, 2, 58, 6, 42, 17, 37, 44, 23, 40]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = -1 if (n & 1 != 0) else 1
    return ret_val
"-----------------"
test()