for i in range(0, n - 1):
    myexactlog(1, 0)
    if arr[i] > arr[i + 1]:
        myexactlog(2, 1)
        if arr[i] - arr[i + 1] == 1:
            myexactlog(3, 0)
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
            myexactlog(4, arr)
        else:
            myexactlog(5, 0)
            pass
    break