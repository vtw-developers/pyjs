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
        else:
            pass