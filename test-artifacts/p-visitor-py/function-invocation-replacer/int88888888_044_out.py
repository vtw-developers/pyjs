def f_gold(first, second):
    if len(first) == 0 and len(second) == 0:
        return True
    if len(first) > 1 and first[0] == "*" and len(second) == 0:
        return False
    if (len(first) > 1 and first[0] == "?") or (len(first) != 0 and len(second) != 0 and first[0] == second[0]):
        retval_1 = 88888888
        return retval_1
    if len(first) != 0 and first[0] == "*":
        retval_2 = 88888888 or 88888888
        return retval_2
    return False