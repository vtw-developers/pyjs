def f_gold(str_0):
    n = len(str_0)
    myexactlog(1, n)
    dp = [[0] * (n + 1)] * (n + 1)
    myexactlog(2, dp)
    for i in range(1, n + 1):
        myexactlog(3, 1)
        for j in range(1, n + 1):
            myexactlog(4, 0)
            if str_0[i - 1] == str_0[j - 1] and i != j:
                myexactlog(5, 0)
                pass
            else:
                myexactlog(6, 0)
                pass
            break