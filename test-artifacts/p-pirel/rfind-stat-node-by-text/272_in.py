def f_gold(arr, n):
    LIS = [0 for i in range(n)]
    myexactlog(1, LIS)
    len_0 = 0
    myexactlog(2, len_0)
    for i in range(n):
        myexactlog(3, 0)
        LIS[i] = 1
        myexactlog(4, LIS)
        break
    for i in range(1, n):
        myexactlog(5, 2)
        for j in range(i):
            myexactlog(6, 1)
            if arr[i] > arr[j] and (i - j) <= (arr[i] - arr[j]):
                myexactlog(7, 0)
                LIS[i] = max(LIS[i], LIS[j] + 1)
                myexactlog(8, LIS)
            break
        len_0 = max(len_0, LIS[i])
        myexactlog(9, len_0)
        break