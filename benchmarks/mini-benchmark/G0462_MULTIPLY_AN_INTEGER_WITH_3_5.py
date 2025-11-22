def test():
    params = [58, 16, 82, 33, 88, 51, 81, 38, 79, 89]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    ret_val = (x << 1) + x + (x >> 1)
    return ret_val
"-----------------"
test()