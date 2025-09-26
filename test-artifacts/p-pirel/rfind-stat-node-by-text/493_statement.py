while k < m and l < n:
    myexactlog(5, 0)
    for i in range(k, m):
        myexactlog(6, 0)
        print(arr[i][l], end=" ")
        cnt += 1
        myexactlog(7, cnt)
        break
    l += 1
    myexactlog(8, l)
    if cnt == total:
        myexactlog(9, 0)
        break
    for i in range(l, n):
        myexactlog(10, 1)
        print(arr[m - 1][i], end=" ")
        cnt += 1
        myexactlog(11, cnt)
        break
    m -= 1
    myexactlog(12, m)
    if cnt == total:
        myexactlog(13, 1)
        pass
    else:
        myexactlog(14, 0)
        pass
    break