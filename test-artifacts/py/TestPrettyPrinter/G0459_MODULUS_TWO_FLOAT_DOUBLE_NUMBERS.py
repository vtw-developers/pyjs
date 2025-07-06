def f_gold(a, b):
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    mod = a
    while mod >= b:
        mod = mod - b
    if a < 0:
        return -mod
    return mod