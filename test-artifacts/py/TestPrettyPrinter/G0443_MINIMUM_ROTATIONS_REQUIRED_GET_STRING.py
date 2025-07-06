def f_gold(str):
    tmp = str + str
    n = len(str)
    for i in range(1, n + 1):
        substring = tmp[i:n]
        if str == substring:
            return i
    return n