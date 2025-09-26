def f_gold(s):
    n = len(s)
    myexactlog(1, n)
    count = 0
    myexactlog(2, count)
    for i in range(0, n, 1):
        myexactlog(3, 0)
        if s[i] == "4" or s[i] == "8" or s[i] == "0":
            myexactlog(4, 0)
            pass