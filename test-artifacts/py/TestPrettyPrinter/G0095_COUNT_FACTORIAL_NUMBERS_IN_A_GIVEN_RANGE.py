def f_gold(low, high):
    fact = 1
    x = 1
    while fact < low:
        fact = fact * x
        x += 1
    res = 0
    while fact <= high:
        res += 1
        fact = fact * x
        x += 1
    return res