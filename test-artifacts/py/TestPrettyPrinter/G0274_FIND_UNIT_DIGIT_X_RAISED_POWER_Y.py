def f_gold(x, y):
    res = 1
    for i in range(y):
        res = (res * x) % 10
    return res