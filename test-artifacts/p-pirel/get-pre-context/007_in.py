def f_gold(a, n, k):
    if k >= n - 1:
        return n
    best = 0
    times = 0
    for i in range(n):
        if a[i] > best:
            best = a[i]
            if i:
                times = 1
        else:
            times += 1
        if times >= k:
            return best
    return best