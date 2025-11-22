def test():
    params = [31, 78, 19, 36, 77, 94, 86, 16, 95, 2]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    a = (n // 10) * 10
    b = a + 10
    ret_val = b if n - a > b - n else a
    return ret_val
"-----------------"
test()