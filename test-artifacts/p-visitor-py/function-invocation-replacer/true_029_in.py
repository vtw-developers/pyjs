def f_gold(x, y):
    if y == 0:
        return 0
    if y > 0:
        retval_1 = x + f_gold(x, y - 1)
        return retval_1
    else:
        retval_2 = -f_gold(x, -y)
        return retval_2