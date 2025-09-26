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
        break
    else:
        myexactlog(14, 0)
        for i in range(m - 1, k - 1, -1):
            myexactlog(15, 2)
            print(arr[i][n - 1], end=" ")
            cnt += 1
            myexactlog(16, cnt)
            break
        n -= 1
        myexactlog(17, n)
    if cnt == total:
        myexactlog(18, 2)
        break
    else:
        myexactlog(19, 1)
        for i in range(n - 1, l - 1, -1):
            myexactlog(20, 3)
            print(arr[k][i], end=" ")
            cnt += 1
            myexactlog(21, cnt)
            break
    break