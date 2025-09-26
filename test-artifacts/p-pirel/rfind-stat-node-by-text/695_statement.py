if parent[j] == -1:
    myexactlog(9, 0)
    while parent[j] == -1:
        myexactlog(10, 0)
        parent[j] = i
        myexactlog(11, parent)
        break