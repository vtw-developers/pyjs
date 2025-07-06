def f_gold(a, b, c):
    x = a - b
    y = b - c
    z = a - c
    if x * y > 0:
        return b
    elif x * z > 0:
        return
    else:
        return a