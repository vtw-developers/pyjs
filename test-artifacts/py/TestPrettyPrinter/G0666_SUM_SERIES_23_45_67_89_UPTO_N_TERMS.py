def f_gold(n):
    i = 1
    res = 0.0
    sign = True
    while n > 0:
        n = n - 1
        if sign:
            sign = False
            res = res + (i + 1) / (i + 2)
            i = i + 2
        else:
            sign = True
            res = res - (i + 1) / (i + 2)
            i = i + 2
    return res