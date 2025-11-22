def test():
    params = [14, 78, 45, 66, 18, 32, 60, 16, 99, 65]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(r):
    ret_val = 2 * r * r
    return ret_val
"-----------------"
test()