def f_gold(n):
    return 1 if (n == 1 or n == 0) else n * f_gold(n - 1)