def f_gold(m, n, arr):
    k = 0
    myexactlog(1, k)
    l = 0
    myexactlog(2, l)
    cnt = 0
    myexactlog(3, cnt)
    total = m * n
    myexactlog(4, total)
    while k < m and l < n:
        myexactlog(5, 0)
        for i in range(k, m):
            myexactlog(6, 0)
            print(arr[i][l], end=" ")
            break
        break