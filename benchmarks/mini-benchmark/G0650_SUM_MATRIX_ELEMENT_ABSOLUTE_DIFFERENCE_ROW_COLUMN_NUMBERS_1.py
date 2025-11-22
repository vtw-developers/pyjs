def test():
    params = [63, 72, 28, 35, 6, 70, 20, 8, 8, 35]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    sum_0 = 0
    for i in range(n):
        sum_0 += i * (n - i)
    ret_val = 2 * sum_0
    return ret_val
"-----------------"
test()