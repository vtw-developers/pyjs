def test():
    params = [90, 95, 22, 29, 62, 40, 52, 21, 33, 11]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = (n * n) + (n * n * n)
    return ret_val
"-----------------"
test()