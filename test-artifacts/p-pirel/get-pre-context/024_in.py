def f_gold(arr, l, r, x):
    if r >= l:
        myexactlog(1, 1)
        mid = l + (r - l) // 2
        myexactlog(2, mid)
        if arr[mid] == x:
            myexactlog(3, 0)
            pass
        elif arr[mid] > x:
            myexactlog(4, 0)
            pass
        else:
            myexactlog(5, 0)
            pass
    else:
        myexactlog(6, 1)
        pass