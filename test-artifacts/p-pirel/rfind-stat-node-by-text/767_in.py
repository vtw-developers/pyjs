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
                    j = (j + A[j] + 1) % n
                    myexactlog(17, j)
                    break