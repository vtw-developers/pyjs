def f_gold(s, c):
    res = 0
    for i in range(len(s)):
        if s[i] == c:
            res = res + 1
    return res