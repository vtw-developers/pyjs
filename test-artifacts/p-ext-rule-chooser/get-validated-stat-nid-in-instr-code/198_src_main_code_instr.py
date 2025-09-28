def f_gold(s):
    if len(s) == 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    ans = 0
    myexactlog(3, ans)
    o = 0
    myexactlog(4, o)
    c = 0
    myexactlog(5, c)
    for i in range(len(s)):
        myexactlog(6, 0)
        if s[i] == "(":
            myexactlog(7, 1)
            o += 1
            myexactlog(8, o)
        if s[i] == ")":
            myexactlog(9, 2)
            c += 1
            myexactlog(10, c)
    if o != c:
        myexactlog(11, 3)
        retval_1 = -1
        myexactlog(12, retval_1)
        myexactlog(13, retval_1)
        return retval_1
    a = [0 for i in range(len(s))]
    myexactlog(14, a)
    if s[0] == "(":
        myexactlog(15, 4)
        a[0] = 1
        myexactlog(16, a)
    else:
        myexactlog(17, 0)
        a[0] = -1
        myexactlog(18, a)
    if a[0] < 0:
        myexactlog(19, 5)
        ans += abs(a[0])
        myexactlog(20, ans)
    for i in range(1, len(s)):
        myexactlog(21, 1)
        if s[i] == "(":
            myexactlog(22, 6)
            pass
        else:
            myexactlog(23, 1)
            pass
        break