def f_gold(arr, n, k):
    if k > n:
        myexactlog(1, 0)
        retval_1 = -1
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    csum = [0] * n
    myexactlog(4, csum)
    csum[0] = arr[0]
    myexactlog(5, csum)
    for i in range(1, n):
        myexactlog(6, 0)
        pass
        break