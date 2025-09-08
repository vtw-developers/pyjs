def f_gold(string_0):
    l = 0
    h = len(string_0) - 1
    while h > l:
        l += 1
        h -= 1
        if string_0[l - 1] != string_0[h + 1]:
            return False
    return True