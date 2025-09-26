def f_gold(n):
    res = list()
    myexactlog(1, res)
    res.append(0)
    myexactlog(2, res)
    res.append(1)
    myexactlog(3, res)
    i = 2
    myexactlog(4, i)
    while i < n + 1:
        myexactlog(5, 0)
        res.append(max(i, (res[int(i / 2)] + res[int(i / 3)] + res[int(i / 4)] + res[int(i / 5)])))
        myexactlog(6, res)
        break