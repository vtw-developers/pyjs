def test():
    params = [30, 25, 69, 39, 14, 60, 89, 27, 29, 29]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = n * (n - 1)
    return ret_val
"-----------------"
test()