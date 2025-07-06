def f_gold(arr, n):
    mp = dict()
    for i in range(n - 1):
        for j in range(i + 1, n):
            mp[arr[i] + arr[j]] = (i, j)
    d = -(10 ** 9)
    for i in range(n - 1):
        for j in range(i + 1, n):
            abs_diff = abs(arr[i] - arr[j])
            if abs_diff in mp.keys():
                p = mp[abs_diff]
                if p[0] != i and p[0] != j and p[1] != i and p[1] != j:
                    d = max(d, max(arr[i], arr[j]))
    return d