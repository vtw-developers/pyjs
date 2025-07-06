def f_gold(x, y, z):
    if not (y / x):
        return y if (not (y / z)) else z
    return x if (not (x / z)) else z