def test():
    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sum_0 = 0
    sum_0 = 1 << n
    ret_val = sum_0 - 1
    return ret_val
"-----------------"
test()