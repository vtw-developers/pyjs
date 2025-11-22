def test():
    params = [98, 9, 18, 38, 84, 8, 39, 6, 60, 47]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(a):
    ret_val = 4 * a
    return ret_val
"-----------------"
test()