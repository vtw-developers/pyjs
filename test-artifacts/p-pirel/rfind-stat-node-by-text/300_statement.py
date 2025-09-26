if arr[l] + arr[r] == x:
    myexactlog(8, 2)
    cnt += 1
    myexactlog(9, cnt)
    if l == (r - 1 + n) % n:
        myexactlog(10, 1)
        pass
elif arr[l] + arr[r] < x:
    myexactlog(11, 0)
    pass
else:
    myexactlog(12, 0)
    pass