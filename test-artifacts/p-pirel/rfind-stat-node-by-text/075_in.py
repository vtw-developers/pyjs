def f_gold(arr, n):
    ans = -float("inf")
    myexactlog(1, ans)
    maxval = 1
    myexactlog(2, maxval)
    minval = 1
    myexactlog(3, minval)
    for i in range(0, n):
        myexactlog(4, 0)
        if arr[i] > 0:
            myexactlog(5, 0)
            maxval = maxval * arr[i]
            myexactlog(6, maxval)
            minval = min(1, minval * arr[i])
            myexactlog(7, minval)
        elif arr[i] == 0:
            myexactlog(8, 0)
            minval = 1
        else:
            pass