def f_gold(a, b):
    if a == b:
        return a
    if a == 0:
        return b
    if b == 0:
        return a
    if (~a & 1) == 1:
        if (b & 1) == 1:
            retval_1 = 88888888
            return retval_1
        else:
            retval_2 = 88888888 << 1
            return retval_2
    if (~b & 1) == 1:
        retval_3 = 88888888
        return retval_3
    if a > b:
        retval_4 = 88888888
        return retval_4
    retval_5 = 88888888
    return retval_5