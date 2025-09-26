for j in range(0, n):
    myexactlog(3, 2)
    if i == j:
        myexactlog(4, 0)
        continue
    for k in range(j + 1, n):
        myexactlog(5, 1)
        if i == k:
            myexactlog(6, 1)
            continue
        for l in range(k + 1, n):
            myexactlog(7, 0)
            if i == l:
                myexactlog(8, 2)
                continue
            break
        break
    break