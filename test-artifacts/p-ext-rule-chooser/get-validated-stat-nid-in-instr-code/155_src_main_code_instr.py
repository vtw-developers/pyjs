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
        pass
        break