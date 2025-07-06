def f_gold(m, n):
    if m < n:
        return 0
    if n == 0:
        return 1
    res = f_gold(m - 1, n) + f_gold(m // 2, n - 1)
    return res