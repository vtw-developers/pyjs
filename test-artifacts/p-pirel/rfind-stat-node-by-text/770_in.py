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
    res = lps[n - 1]
    myexactlog(16, res)
    if res > n / 2:
        myexactlog(17, 2)
        retval_1 = n // 2
        myexactlog(18, retval_1)
        myexactlog(19, retval_1)
        return retval_1
    else:
        myexactlog(20, 2)
        pass