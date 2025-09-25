def f_gold(high, low, n):
    if n <= 0:
        return 0
    retval_1 = max(high[n - 1] + f_gold(high, low, (n - 2)), low[n - 1] + f_gold(high, low, (n - 1)))
    return retval_1