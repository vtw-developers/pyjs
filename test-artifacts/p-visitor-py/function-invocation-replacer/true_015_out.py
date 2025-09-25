def f_gold(num):
    if num < 0:
        retval_1 = True
        return retval_1
    if num == 0 or num == 7:
        return True
    if num < 10:
        return False
    retval_2 = True
    return retval_2