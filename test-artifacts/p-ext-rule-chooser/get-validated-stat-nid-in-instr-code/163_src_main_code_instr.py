def f_gold(arr, n, m):
    if m == 0 or n == 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    arr.sort()
    myexactlog(3, arr)
    if n < m:
        myexactlog(4, 1)
        retval_1 = -1
        myexactlog(5, retval_1)
        myexactlog(6, retval_1)
        return retval_1
    min_diff = sys.maxsize
    myexactlog(7, min_diff)
    first = 0
    myexactlog(8, first)
    last = 0
    myexactlog(9, last)
    i = 0
    myexactlog(10, i)
    while i + m - 1 < n:
        myexactlog(11, 0)
        diff = arr[i + m - 1] - arr[i]
        myexactlog(12, diff)
        if diff < min_diff:
            myexactlog(13, 2)
            min_diff = diff
            myexactlog(14, min_diff)
            first = i
            myexactlog(15, first)
            last = i + m - 1
            myexactlog(16, last)
        i += 1
        myexactlog(17, i)
    retval_2 = arr[last] - arr[first]
    myexactlog(18, retval_2)
    myexactlog(19, retval_2)
    return retval_2