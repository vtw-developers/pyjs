def f_gold(arr, n, m):
    if m == 0 or n == 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    arr.sort()
    myexactlog(3, arr)