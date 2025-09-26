while l != r:
    myexactlog(6, 0)
    if arr[l] + arr[r] == x:
        myexactlog(7, 1)
        myexactlog(8, True)
        return True
    if arr[l] + arr[r] < x:
        myexactlog(9, 2)
        l = (l + 1) % n
        myexactlog(10, l)
    else:
        myexactlog(11, 0)
        r = (n + r - 1) % n
        myexactlog(12, r)
    break