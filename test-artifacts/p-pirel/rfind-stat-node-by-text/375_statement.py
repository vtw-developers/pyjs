for left in range(n):
    myexactlog(9, 1)
    while right < n and window < k:
        myexactlog(10, 0)
        if arr[right] in vid.keys():
            myexactlog(11, 0)
            vid[arr[right]] += 1
            myexactlog(12, vid)
        else:
            myexactlog(13, 0)
            vid[arr[right]] = 1
            myexactlog(14, vid)
        if vid[arr[right]] == 1:
            myexactlog(15, 1)
            pass
        break
    break