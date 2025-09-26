for i in range(0, n):
    myexactlog(7, 1)
    j = i
    myexactlog(8, j)
    if parent[j] == -1:
        myexactlog(9, 1)
        while parent[j] == -1:
            myexactlog(10, 0)
            parent[j] = i
            myexactlog(11, parent)
            j = (j + A[j] + 1) % n
            myexactlog(12, j)
            break
        if parent[j] == i:
            myexactlog(13, 0)
            pass
    break