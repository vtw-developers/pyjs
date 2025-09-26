if i > m:
    myexactlog(6, 0)
    count[i] = count[i - 1] + count[i - m]
    myexactlog(7, count)
elif i < m:
    myexactlog(8, 0)
    pass
else:
    myexactlog(9, 0)
    pass