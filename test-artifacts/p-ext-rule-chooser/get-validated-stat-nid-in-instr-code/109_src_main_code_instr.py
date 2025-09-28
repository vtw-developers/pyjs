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
    for j in range(i, n):
        myexactlog(6, 1)
        if str_0[j] != "b":
            myexactlog(7, 2)
            myexactlog(8, False)
            return False
    myexactlog(9, True)
    return True