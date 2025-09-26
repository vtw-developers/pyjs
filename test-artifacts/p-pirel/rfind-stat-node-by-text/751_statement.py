if parent[j] == -1:
    while parent[j] == -1:
        parent[j] = i
        j = (j + A[j] + 1) % n
    if parent[j] == i:
        while vis[j] == 0:
            vis[j] = 1
            cnt = cnt + 1
            j = (j + A[j] + 1) % n