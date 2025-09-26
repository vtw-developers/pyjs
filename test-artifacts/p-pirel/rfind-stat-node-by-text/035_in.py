def f_gold(arr, n):
    for i in range(0, n):
        myexactlog(1, 0)
        if arr[i] & 1:
            myexactlog(2, 0)
            arr[i] *= -1
            myexactlog(3, arr)
        break
    arr.sort()
    myexactlog(4, arr)
    for i in range(0, n):
        myexactlog(5, 1)
        if arr[i] & 1:
            myexactlog(6, 1)
            arr[i] *= -1