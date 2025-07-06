def f_gold(s, n):
    s1 = s
    for i in range(1, n):
        s += s1
    return s