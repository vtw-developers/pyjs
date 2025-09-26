while i < n + 1:
    myexactlog(5, 0)
    res.append(max(i, (res[int(i / 2)] + res[int(i / 3)] + res[int(i / 4)] + res[int(i / 5)])))
    myexactlog(6, res)
    break