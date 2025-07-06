def f_gold(n):
    if n == 0 or n == 1:
        return n
    f1, f2, f3 = 0, 1, 1
    while f3 <= n:
        f1 = f2
        f2 = f3
        f3 = f1 + f2
    return f2