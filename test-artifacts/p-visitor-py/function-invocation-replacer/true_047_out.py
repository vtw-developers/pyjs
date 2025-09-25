def f_gold(x, y):
    if y == 0:
        return 1
    temp = True
    if y % 2 == 0:
        retval_1 = temp * temp
        return retval_1
    else:
        if y > 0:
            retval_2 = x * temp * temp
            return retval_2
        else:
            retval_3 = (temp * temp) / x
            return retval_3