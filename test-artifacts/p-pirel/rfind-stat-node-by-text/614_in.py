def f_gold(A, n):
    cnt = 0
    myexactlog(1, cnt)
    parent = [None] * (n + 1)
    myexactlog(2, parent)
    vis = [None] * (n + 1)
    myexactlog(3, vis)
    for i in range(0, n + 1):
        myexactlog(4, 0)
        parent[i] = -1
        myexactlog(5, parent)
        vis[i] = 0
        myexactlog(6, vis)
        break
    for i in range(0, n):
        myexactlog(7, 1)
        j = i
        myexactlog(8, j)
        break