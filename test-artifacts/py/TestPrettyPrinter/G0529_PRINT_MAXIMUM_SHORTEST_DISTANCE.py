def f_gold(a, n, k):
    b = dict()
    for i in range(n):
        x = a[i]
        d = min(1 + i, n - i)
        if x not in b.keys():
            b[x] = d
        else:
            b[x] = min(d, b[x])
    ans = 10 ** 9
    for i in range(n):
        x = a[i]
        if x != (k - x) and (k - x) in b.keys():
            ans = min(max(b[x], b[k - x]), ans)
    return ans