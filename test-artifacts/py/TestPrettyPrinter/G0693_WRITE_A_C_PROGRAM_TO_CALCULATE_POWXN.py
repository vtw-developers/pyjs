def f_gold(x, y):
    if y == 0:
        return 1
    elif int(y % 2) == 0:
        return f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
    else:
        return x * f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))