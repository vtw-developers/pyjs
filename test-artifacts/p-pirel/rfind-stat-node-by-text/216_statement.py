if arr[i] == 0:
    myexactlog(3, 0)
    jumps[i] = float("inf")
    myexactlog(4, jumps)
elif arr[i] >= n - i - 1:
    myexactlog(5, 0)
    pass
else:
    myexactlog(6, 0)
    pass