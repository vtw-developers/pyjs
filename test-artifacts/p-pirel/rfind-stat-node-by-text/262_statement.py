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