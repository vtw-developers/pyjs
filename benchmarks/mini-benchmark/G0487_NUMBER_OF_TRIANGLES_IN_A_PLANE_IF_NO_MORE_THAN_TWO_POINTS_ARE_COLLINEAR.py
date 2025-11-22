def test():
    params = [67, 58, 67, 60, 4, 97, 9, 16, 83, 87]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = n * (n - 1) * (n - 2) // 6
    return ret_val
"-----------------"
test()