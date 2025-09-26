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
        while vis[j] == 0:
            myexactlog(14, 1)
            vis[j] = 1
            myexactlog(15, vis)
            cnt = cnt + 1
            myexactlog(16, cnt)
            break