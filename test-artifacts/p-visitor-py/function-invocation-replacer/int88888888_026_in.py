def f_gold(n):
    if n == 1:
        return 2
    retval_1 = 2 * f_gold(n - 1)
    return retval_1