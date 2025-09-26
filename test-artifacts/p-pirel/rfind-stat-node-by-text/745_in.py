def f_gold(arr, n, x):
    i = 0
    myexactlog(1, i)
    while i < n:
        myexactlog(2, 0)
        if arr[i] == x:
            myexactlog(3, 0)
            myexactlog(4, i)
            return i
        i = i + abs(arr[i] - x)
        myexactlog(5, i)
        break