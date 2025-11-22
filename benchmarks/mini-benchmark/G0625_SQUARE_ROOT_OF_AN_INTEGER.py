def test():
    params = [89, 11, 14, 92, 76, 63, 51, 16, 83, 66, 0]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    if x == 0 or x == 1:
        return x
    i = 1
    result = 1
    while result <= x:
        i += 1
        result = i * i
    ret_val = i - 1
    return ret_val
"-----------------"
test()