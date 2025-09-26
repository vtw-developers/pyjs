def f_gold(arr, n, m):
    if n > m:
        myexactlog(1, 0)
        myexactlog(2, True)
        return True
    DP = [False for i in range(m)]
    myexactlog(3, DP)
    for i in range(n):
        myexactlog(4, 1)
        if DP[0]:
            myexactlog(5, 1)
            myexactlog(6, True)
            return True
        temp = [False for i in range(m)]
        myexactlog(7, temp)
        for j in range(m):
            myexactlog(8, 0)
            if DP[j] == True:
                myexactlog(9, 3)
                if DP[(j + arr[i]) % m] == False:
                    myexactlog(10, 2)
                    pass