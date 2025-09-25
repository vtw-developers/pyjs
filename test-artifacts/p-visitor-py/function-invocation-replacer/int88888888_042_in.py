def f_gold(n):
    if n == 0:
        return 1
    retval_1 = n * f_gold(n - 1)
    return retval_1