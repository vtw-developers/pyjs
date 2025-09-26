for i in range(n, 0, -1):
    myexactlog(4, 1)
    if not (i % 2):
        myexactlog(5, 0)
        table[i // 2] = min(table[i] + 1, table[i // 2])
        myexactlog(6, table)
    if not (i % 3):
        myexactlog(7, 1)
        pass
    break