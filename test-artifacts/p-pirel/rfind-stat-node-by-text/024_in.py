def f_gold(a, b):
    if a == b:
        myexactlog(1, 0)
        myexactlog(2, a)
        return a
    if a == 0:
        myexactlog(3, 1)
        myexactlog(4, b)
        return b
    if b == 0:
        myexactlog(5, 2)
        myexactlog(6, a)
        return a