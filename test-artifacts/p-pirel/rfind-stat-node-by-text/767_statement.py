while vis[j] == 0:
    myexactlog(14, 1)
    vis[j] = 1
    myexactlog(15, vis)
    cnt = cnt + 1
    myexactlog(16, cnt)
    j = (j + A[j] + 1) % n
    myexactlog(17, j)
    break