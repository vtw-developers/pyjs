def f_gold(A, n):
    cnt = 0
    parent = [None] * (n + 1)
    vis = [None] * (n + 1)
    for i in range(0, n + 1):
        parent[i] = -1
        vis[i] = 0
    for i in range(0, n):
        j = i
        if parent[j] == -1:
            while parent[j] == -1:
                parent[j] = i
                j = (j + A[j] + 1) % n
            if parent[j] == i:
                while vis[j] == 0:
                    vis[j] = 1
                    cnt = cnt + 1
                    j = (j + A[j] + 1) % n