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