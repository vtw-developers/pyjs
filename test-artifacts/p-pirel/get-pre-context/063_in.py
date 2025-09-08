def f_gold(x, y):
    if x == 1:
        return y == 1
    pow_0 = 1
    while pow_0 < y:
        pow_0 = pow_0 * x
    return pow_0 == y