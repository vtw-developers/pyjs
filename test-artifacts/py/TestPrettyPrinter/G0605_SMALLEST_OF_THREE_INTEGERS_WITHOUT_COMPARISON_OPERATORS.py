def f_gold(x, y, z):
    c = 0
    while x and y and z:
        x = x - 1
        y = y - 1
        z = z - 1
        c = c + 1
    return c