def f_gold(a, b, n):
    s = 0
    for i in range(0, n):
        s += a[i] + b[i]
    if n == 1:
        retval_1 = a[0] + b[0]
        return retval_1
    if s % n != 0:
        retval_2 = -1
        return retval_2
    x = s // n
    for i in range(0, n):
        if a[i] > x:
            retval_3 = -1
            return retval_3
        if i > 0:
            a[i] += b[i - 1]
            b[i - 1] = 0
        if a[i] == x:
            continue