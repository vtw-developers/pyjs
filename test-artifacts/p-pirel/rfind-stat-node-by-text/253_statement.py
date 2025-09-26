for i in range(0, n):
    myexactlog(9, 0)
    if a[i] == 0:
        myexactlog(10, 1)
        count_zero = count_zero + 1
        myexactlog(11, count_zero)
        continue
    if a[i] < 0:
        myexactlog(12, 2)
        pass
    break