def f_gold(a, b, n):
    s = 0
    for i in range(0, n):
        s += a[i] + b[i]
    if n == 1:
        return a[0] + b[0]
    if s % n != 0:
        return -1
    x = s // n
    for i in range(0, n):
        if a[i] > x:
            return -1
        if i > 0:
            a[i] += b[i - 1]
            b[i - 1] = 0
        if a[i] == x:
            continue
        y = a[i] + b[i]
        if i + 1 < n:
            y += b[i + 1]
        if y == x:
            a[i] = y
            b[i] = 0
            if i + 1 < n:
                b[i + 1] = 0
            continue
        if a[i] + b[i] == x:
            a[i] += b[i]
            b[i] = 0
            continue
        if i + 1 < n and a[i] + b[i + 1] == x:
            a[i] += b[i + 1]
            b[i + 1] = 0
            continue
        return -1
    for i in range(0, n):
        if b[i] != 0:
            return -1
    return x