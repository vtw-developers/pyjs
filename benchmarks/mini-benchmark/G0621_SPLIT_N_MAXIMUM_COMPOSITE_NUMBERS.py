def test():
    params = [55, 35, 24, 75, 5, 7, 50, 28, 67, 59, 3, 9, 15]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    if n < 4:
        return -1
    rem = n % 4
    if rem == 0:
        ret_val1 = n // 4
        return ret_val1
    if rem == 1:
        if n < 9:
            return -1
        ret_val2 = (n - 9) // 4 + 1
        return ret_val2
    if rem == 2:
        ret_val3 = (n - 6) // 4 + 1
        return ret_val3
    else:
        if n < 15:
            return -1
        ret_val4 = (n - 15) // 4 + 2
        return ret_val4
"-----------------"
test()