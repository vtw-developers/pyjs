if l != 0:
    myexactlog(11, 0)
    l = lps[l - 1]
    myexactlog(12, l)
else:
    myexactlog(13, 0)
    lps[i] = 0
    myexactlog(14, lps)