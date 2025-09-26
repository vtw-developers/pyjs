if arr[l] + arr[r] == x:
    myexactlog(8, 2)
    cnt += 1
    myexactlog(9, cnt)
    if l == (r - 1 + n) % n:
        myexactlog(10, 1)
        myexactlog(11, cnt)
        return cnt
    l = (l + 1) % n
    myexactlog(12, l)
    r = (r - 1 + n) % n
    myexactlog(13, r)
elif arr[l] + arr[r] < x:
    myexactlog(14, 0)
    l = (l + 1) % n
    myexactlog(15, l)
else:
    myexactlog(16, 0)
    pass