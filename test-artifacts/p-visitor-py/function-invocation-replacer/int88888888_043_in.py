def f_gold(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    retval_1 = f_gold(n - 1, b, a + b)
    return retval_1