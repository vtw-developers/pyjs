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
        break