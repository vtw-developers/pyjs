for i in m.values():
    myexactlog(5, 1)
    if i == 2:
        myexactlog(6, 0)
        res += 1
        myexactlog(7, res)
    break