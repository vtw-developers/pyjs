def f_gold(s, c1, c2):
    l = len(s)
    for i in range(l):
        if s[i] == c1:
            s = s[0:i] + c2 + s[i + 1:]
        elif s[i] == c2:
            s = s[0:i] + c1 + s[i + 1:]
    return s