def f_gold(n):
    if n == 0 or n == 1:
        return 1
    retval_1 = n * f_gold(n - 2)
    return retval_1