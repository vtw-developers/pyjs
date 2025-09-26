def f_gold(arr, n):
    for i in range(0, n - 1):
        myexactlog(1, 0)
        if arr[i] > arr[i + 1]:
            myexactlog(2, 0)
            pass
        break