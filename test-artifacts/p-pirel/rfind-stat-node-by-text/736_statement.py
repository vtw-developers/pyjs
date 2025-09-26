while b != 0:
    myexactlog(12, 3)
    while (b & 1) == 0:
        myexactlog(13, 2)
        b = b >> 1
        myexactlog(14, b)
        break
    break