def f_gold(n):
    if n == 1:
        return 2
    return 2 * f_gold(n - 1)