def f_gold(a, b, n, k):
    a.sort(reverse=True)
    b.sort()
    for i in range(n):
        if a[i] + b[i] < k:
            return False
    return True