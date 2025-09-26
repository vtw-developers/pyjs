def f_gold(s):
    n = len(s)
    myexactlog(1, n)
    s1 = ""
    myexactlog(2, s1)
    s1 = s1 + s[0].lower()
    myexactlog(3, s1)
    i = 1
    myexactlog(4, i)
    while i < n:
        myexactlog(5, 0)
        if s[i] == " " and i <= n:
            myexactlog(6, 0)
            pass
        else:
            myexactlog(7, 0)
            pass