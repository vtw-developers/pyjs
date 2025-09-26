def f_gold(arr, n, k):
    if n == 1:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    arr.sort()
    myexactlog(3, arr)
    ans = arr[n - 1] - arr[0]
    myexactlog(4, ans)
    small = arr[0] + k
    myexactlog(5, small)
    big = arr[n - 1] - k
    myexactlog(6, big)
    if small > big:
        myexactlog(7, 1)
        small, big = big, small
        myexactlog(8, small, big)
    for i in range(1, n - 1):
        myexactlog(9, 0)
        subtract = arr[i] - k
        myexactlog(10, subtract)
        add = arr[i] + k
        myexactlog(11, add)
        if subtract >= small or add <= big:
            myexactlog(12, 2)
            continue
        if big - subtract <= add - small:
            myexactlog(13, 3)
            pass
        else:
            myexactlog(14, 0)
            pass