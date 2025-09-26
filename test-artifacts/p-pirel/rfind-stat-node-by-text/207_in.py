def f_gold(k, n):
    f1 = 0
    f2 = 1
    f3 = f1 + f2
    i = 2
    while f3 % k != 0:
        f1 = f2
        f2 = f3
        f3 = f1 + f2