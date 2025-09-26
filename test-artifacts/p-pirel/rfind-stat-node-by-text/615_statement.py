for i in range(2, d + 1):
    myexactlog(8, 0)
    a[i] = a[i - 1] * 10 + 45 * int(math.ceil(math.pow(10, i - 1)))
    myexactlog(9, a)
    break