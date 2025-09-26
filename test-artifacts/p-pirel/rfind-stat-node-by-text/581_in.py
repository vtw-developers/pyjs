def f_gold(arr, n):
    inc, dcr = dict(), dict()
    myexactlog(1, inc, dcr)
    len_inc, len_dcr = [0] * n, [0] * n
    myexactlog(2, len_inc, len_dcr)
    longLen = 0
    myexactlog(3, longLen)
    for i in range(n):
        myexactlog(4, 0)
        len_0 = 0
        myexactlog(5, len_0)
        if inc.get(arr[i] - 1) in inc.values():
            myexactlog(6, 0)
            len_0 = inc.get(arr[i] - 1)
            myexactlog(7, len_0)
        inc[arr[i]] = len_inc[i] = len_0 + 1
        myexactlog(8, inc)
        break
    for i in range(n - 1, -1, -1):
        myexactlog(9, 1)
        len_0 = 0
        myexactlog(10, len_0)
        if dcr.get(arr[i] - 1) in dcr.values():
            myexactlog(11, 1)
            len_0 = dcr.get(arr[i] - 1)
            myexactlog(12, len_0)
        dcr[arr[i]] = len_dcr[i] = len_0 + 1
        myexactlog(13, dcr)
        break
    for i in range(n):
        myexactlog(14, 2)
        if longLen < (len_inc[i] + len_dcr[i] - 1):
            myexactlog(15, 2)
            longLen = len_inc[i] + len_dcr[i] - 1
            myexactlog(16, longLen)