def test():
    params = [41, 42, 62, 4, 31, 75, 5, 75, 85, 19]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = (n << 3) - n
    return ret_val
"-----------------"
test()