def f_gold(str_0):
    n = len(str_0)
    myexactlog(1, n)
    for i in range(n):
        myexactlog(2, 0)
        if str_0[i] != "a":
            myexactlog(3, 0)
            break
    if i * 2 != n:
        myexactlog(4, 1)
        myexactlog(5, False)
        return False