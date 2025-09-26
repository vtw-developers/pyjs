for i in Hash:
    myexactlog(9, 1)
    if max_count < Hash[i]:
        myexactlog(10, 1)
        res = i
        myexactlog(11, res)
        max_count = Hash[i]
        myexactlog(12, max_count)
    break