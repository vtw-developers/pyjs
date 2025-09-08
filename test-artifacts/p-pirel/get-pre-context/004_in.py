def f_gold(x, y):
    while y != 0:
        carry = x & y
        x = x ^ y
        y = carry << 1
    return x