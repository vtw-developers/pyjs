def f_gold(n, x, y):
    arr = [False for i in range(n + 2)]
    myexactlog(1, arr)
    if x <= n:
        myexactlog(2, 0)
        pass