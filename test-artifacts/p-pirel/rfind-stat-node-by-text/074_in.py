def f_gold(n, x, y):
    arr = [False for i in range(n + 2)]
    myexactlog(1, arr)
    if x <= n:
        myexactlog(2, 0)
        arr[x] = True
        myexactlog(3, arr)
    if y <= n:
        myexactlog(4, 1)
        arr[y] = True
        myexactlog(5, arr)
    result = 0
    myexactlog(6, result)
    for i in range(min(x, y), n + 1):
        myexactlog(7, 0)
        if arr[i]:
            myexactlog(8, 4)
            if i + x <= n:
                myexactlog(9, 2)
                arr[i + x] = True