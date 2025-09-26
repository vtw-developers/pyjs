def f_gold(x):
    temp = x
    myexactlog(1, temp)
    n = 0
    myexactlog(2, n)
    while x != 0:
        myexactlog(3, 0)
        x = x // 10
        myexactlog(4, x)
        n = n + 1
        myexactlog(5, n)
        break
    x = temp
    myexactlog(6, x)
    sm = 0
    myexactlog(7, sm)
    while x != 0:
        myexactlog(8, 1)
        sm = sm + int(math.pow(x % 10, n))
        myexactlog(9, sm)
        x = x // 10