def f_gold(x):
    m = 1
    while x & m:
        x = x ^ m
        m <<= 1
    x = x ^ m
    return x