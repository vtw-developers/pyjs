def test():
    params = [57, 96, 14, 64, 24, 74, 85, 27, 78, 1]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(k):
    ret_val = k * k * k
    return ret_val
"-----------------"
test()