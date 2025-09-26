while i < n:
    myexactlog(5, 0)
    if s[i] == s[l]:
        myexactlog(6, 1)
        l = l + 1
        myexactlog(7, l)
        lps[i] = l
        myexactlog(8, lps)
        i = i + 1
        myexactlog(9, i)
    else:
        myexactlog(10, 1)
        if l != 0:
            myexactlog(11, 0)
            l = lps[l - 1]
            myexactlog(12, l)
        else:
            myexactlog(13, 0)
            lps[i] = 0
            myexactlog(14, lps)
            i = i + 1
            myexactlog(15, i)
    break