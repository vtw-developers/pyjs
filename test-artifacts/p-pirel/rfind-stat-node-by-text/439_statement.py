for i in range(0, n):
    myexactlog(9, 0)
    if a[i] == 0:
        myexactlog(10, 1)
        count_zero = count_zero + 1
        myexactlog(11, count_zero)
        continue
    if a[i] < 0:
        myexactlog(12, 2)
        count_neg = count_neg + 1
        myexactlog(13, count_neg)
        max_neg = max(max_neg, a[i])
        myexactlog(14, max_neg)
    if a[i] > 0:
        myexactlog(15, 3)
        min_pos = min(min_pos, a[i])
        myexactlog(16, min_pos)
    prod = prod * a[i]
    myexactlog(17, prod)
    break