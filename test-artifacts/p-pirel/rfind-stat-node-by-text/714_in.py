def f_gold(arr, n):
    for i in range(0, n - 1):
        myexactlog(1, 0)
        if arr[i] > arr[i + 1]:
            myexactlog(2, 1)
            if arr[i] - arr[i + 1] == 1:
                myexactlog(3, 0)
                pass
            else:
                myexactlog(4, 0)
                pass