def f_gold(stri, n):
    m = dict()
    myexactlog(1, m)
    for i in range(n):
        myexactlog(2, 0)
        m[stri[i]] = m.get(stri[i], 0) + 1
        myexactlog(3, m)
        break
    res = 0
    myexactlog(4, res)
    for i in m.values():
        myexactlog(5, 1)
        if i == 2:
            myexactlog(6, 0)
            res += 1
            myexactlog(7, res)
        break