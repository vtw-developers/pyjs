def f_gold(s):
    n = len(s)
    myexactlog(1, n)
    lps = [0] * n
    myexactlog(2, lps)
    l = 0
    myexactlog(3, l)
    i = 1
    myexactlog(4, i)
    while i < n:
        myexactlog(5, 0)
        if s[i] == s[l]:
            myexactlog(6, 0)
            l = l + 1
            myexactlog(7, l)
            lps[i] = l
            myexactlog(8, lps)
        else:
            myexactlog(9, 0)
            pass
        break