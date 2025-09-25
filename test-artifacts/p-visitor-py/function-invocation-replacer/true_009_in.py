def f_gold(n):
    if n == 0:
        return 0
    else:
        return 1 + f_gold(n & (n - 1))