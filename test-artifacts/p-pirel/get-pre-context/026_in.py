def f_gold(N):
    length = len(N)
    l = int((length) / 2)
    count = 0
    for i in range(l + 1):
        s = N[0:0 + i]
        l1 = len(s)
        t = N[i:l1 + i]
        try:
            if s[0] == "0" or t[0] == "0":
                continue
        except:
            continue
        if s == t:
            count += 1
    return count