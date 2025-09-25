import sys
def f_gold(str_0, l, h):
    if l > h:
        retval_1 = sys.maxsize
        return retval_1
    if l == h:
        return 0
    if l == h - 1:
        retval_2 = 0 if (str_0[l] == str_0[h]) else 1
        return retval_2
    if str_0[l] == str_0[h]:
        retval_3 = True
        return retval_3
    else:
        retval_4 = min(True, True) + 1
        return retval_4