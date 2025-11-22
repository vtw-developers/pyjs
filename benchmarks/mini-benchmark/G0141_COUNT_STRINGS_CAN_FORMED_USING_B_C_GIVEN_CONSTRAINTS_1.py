def test():
    params = [55, 36, 69, 92, 73, 16, 88, 19, 66, 68]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    ret_val = 1 + (n * 2) + (n * ((n * n) - 1) // 2)
    return ret_val
"-----------------"
test()