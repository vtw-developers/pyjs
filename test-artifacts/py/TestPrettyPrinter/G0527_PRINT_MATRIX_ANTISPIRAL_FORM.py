def f_gold(m, n, a):
    k = 0
    l = 0
    stk = []
    while k <= m and l <= n:
        for i in range(l, n + 1):
            stk.append(a[k][i])
        k += 1
        for i in range(k, m + 1):
            stk.append(a[i][n])
        n -= 1
        if k <= m:
            for i in range(n, l - 1, -1):
                stk.append(a[m][i])
            m -= 1
        if l <= n:
            for i in range(m, k - 1, -1):
                stk.append(a[i][l])
            l += 1
    while len(stk) != 0:
        print(str(stk[-1]), end=" ")
        stk.pop()