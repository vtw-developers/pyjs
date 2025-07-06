def f_gold(s):
    l = len(s)
    s1 = ""
    if l % 2 == 0:
        isEven = True
    else:
        isEven = False
    for i in range(0, l, 2):
        if isEven:
            s1 = s[i] + s1
            s1 += s[i + 1]
        else:
            if l - i > 1:
                s1 += s[i]
                s1 = s[i + 1] + s1
            else:
                s1 += s[i]
    return s1