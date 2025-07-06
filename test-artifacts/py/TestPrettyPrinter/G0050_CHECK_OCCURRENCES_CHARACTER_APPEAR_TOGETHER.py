def f_gold(s, c):
    oneSeen = False
    i = 0
    n = len(s)
    while i < n:
        if s[i] == c:
            if oneSeen == True:
                return False
            while i < n and s[i] == c:
                i = i + 1
            oneSeen = True
        else:
            i = i + 1
    return True