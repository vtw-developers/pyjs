def f_gold(a, b, n):
    a.sort(reverse=False)
    b.sort(reverse=False)
    result = 0
    for i in range(0, n, 1):
        if a[i] > b[i]:
            result = result + abs(a[i] - b[i])
        elif a[i] < b[i]:
            result = result + abs(a[i] - b[i])
    return result