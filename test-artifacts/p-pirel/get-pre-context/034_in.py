def f_gold(str_0):
    res = ord(str_0[0]) - 48
    for i in range(1, len(str_0)):
        if str_0[i] == "0" or str_0[i] == "1" or res < 2:
            res += ord(str_0[i]) - 48
        else:
            res *= ord(str_0[i]) - 48
    return res