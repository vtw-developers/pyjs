def f_gold(a, n):
    if n == 1:
        myexactlog(1, 0)
        retval_1 = a[0]
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    max_neg = float("-inf")
    myexactlog(4, max_neg)
    min_pos = float("inf")
    myexactlog(5, min_pos)
    count_neg = 0
    myexactlog(6, count_neg)
    count_zero = 0
    myexactlog(7, count_zero)
    prod = 1
    myexactlog(8, prod)
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
    if count_zero == n or (count_neg == 0 and count_zero > 0):
        myexactlog(18, 4)
        myexactlog(19, 0)
        return 0
    if count_neg == 0:
        myexactlog(20, 5)
        myexactlog(21, min_pos)
        return min_pos