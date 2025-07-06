def f_gold(a, n):
    a.sort()
    s = []
    i = 0
    j = n - 1
    while i < j:
        s.append((a[i] + a[j]))
        i += 1
        j -= 1
    mini = min(s)
    maxi = max(s)
    return abs(maxi - mini)