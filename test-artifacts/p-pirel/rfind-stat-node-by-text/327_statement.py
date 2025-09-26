while b != 0:
    myexactlog(12, 3)
    while (b & 1) == 0:
        myexactlog(13, 2)
        b = b >> 1
        myexactlog(14, b)
        break
    if a > b:
        myexactlog(15, 2)
        temp = a
        myexactlog(16, temp)
        a = b
        myexactlog(17, a)
    break