def f_gold(str_0, corner):
    n = len(str_0)
    cl = len(corner)
    if n < cl:
        return False
    retval_1 = (str_0[:cl] == corner) and (str_0[n - cl:] == corner)
    return retval_1