def f_gold(str):
    for i in range(0, len(str)):
        if str[i].istitle():
            return str[i]
    return 0