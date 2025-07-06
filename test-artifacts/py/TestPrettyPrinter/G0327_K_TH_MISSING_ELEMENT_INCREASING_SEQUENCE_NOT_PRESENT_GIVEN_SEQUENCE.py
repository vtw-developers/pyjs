def f_gold(a, b, k, n1, n2):
    s = set()
    for i in range(n2):
        s.add(b[i])
    missing = 0
    for i in range(n1):
        if a[i] not in s:
            missing += 1
        if missing == k:
            return a[i]
    return -1