def f_gold(m, n, arr):
    k = 0
    l = 0
    cnt = 0
    total = m * n
    while k < m and l < n:
        for i in range(k, m):
            print(arr[i][l], end=" ")
            cnt += 1
        l += 1
        if cnt == total:
            break
        for i in range(l, n):
            print(arr[m - 1][i], end=" ")
            cnt += 1
        m -= 1
        if cnt == total:
            break
        else:
            for i in range(m - 1, k - 1, -1):
                print(arr[i][n - 1], end=" ")
                cnt += 1
            n -= 1
        if cnt == total:
            break
        else:
            for i in range(n - 1, l - 1, -1):
                print(arr[k][i], end=" ")
                cnt += 1