while l != r:
    myexactlog(6, 0)
    if arr[l] + arr[r] == x:
        myexactlog(7, 1)
        myexactlog(8, True)
        return True
    break