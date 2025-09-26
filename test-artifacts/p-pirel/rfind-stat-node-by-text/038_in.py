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