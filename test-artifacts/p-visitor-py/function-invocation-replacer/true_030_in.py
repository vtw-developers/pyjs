def f_gold(n):
    retval_1 = 1 if (n == 1 or n == 0) else n * f_gold(n - 1)
    return retval_1