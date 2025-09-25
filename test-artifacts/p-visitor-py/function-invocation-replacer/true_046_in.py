def f_gold(x, y):
    if y == 0:
        return 1
    elif int(y % 2) == 0:
        retval_1 = f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
        return retval_1
    else:
        retval_2 = x * f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
        return retval_2