def test():
    params = [38, 44, 58, 10, 31, 53, 94, 64, 71, 59]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = n * (2 * n - 1)
    return ret_val
"-----------------"
test()