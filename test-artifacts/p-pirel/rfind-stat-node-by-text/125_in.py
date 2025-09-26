def f_gold(arr, n):
    msis = [None] * n
    myexactlog(1, msis)
    msds = [None] * n
    myexactlog(2, msds)
    max_sum = 0
    myexactlog(3, max_sum)
    msis[0] = arr[0]
    myexactlog(4, msis)
    for i in range(1, n):
        myexactlog(5, 0)
        if arr[i] > arr[i - 1]:
            myexactlog(6, 0)
            msis[i] = msis[i - 1] + arr[i]
            myexactlog(7, msis)
        else:
            myexactlog(8, 0)
            msis[i] = arr[i]
            myexactlog(9, msis)
        break
    msds[n - 1] = arr[n - 1]
    myexactlog(10, msds)
    for i in range(n - 2, -1, -1):
        myexactlog(11, 1)
        if arr[i] > arr[i + 1]:
            myexactlog(12, 1)
            msds[i] = msds[i + 1] + arr[i]
        else:
            pass