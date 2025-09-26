def f_gold(str_0):
    one_count = 0
    myexactlog(1, one_count)
    zero_count = 0
    myexactlog(2, zero_count)
    n = len(str_0)
    myexactlog(3, n)
    for i in range(0, n, 1):
        myexactlog(4, 0)
        if str_0[i] == "1":
            myexactlog(5, 0)
            one_count += 1
        else:
            pass