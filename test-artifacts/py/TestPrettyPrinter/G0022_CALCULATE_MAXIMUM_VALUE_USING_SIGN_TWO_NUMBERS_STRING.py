def f_gold(str):
    res = ord(str[0]) - 48
    for i in range(1, len(str)):
        if str[i] == "0" or str[i] == "1" or res < 2:
            res += ord(str[i]) - 48
        else:
            res *= ord(str[i]) - 48
    return res