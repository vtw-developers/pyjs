def f_gold(a, n):
    if n == 1:
        myexactlog(1, 0)
        retval_1 = a[0]
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    max_neg = -999999999999
    myexactlog(4, max_neg)
    count_neg = 0
    myexactlog(5, count_neg)
    count_zero = 0
    myexactlog(6, count_zero)
    prod = 1
    myexactlog(7, prod)
    for i in range(n):
        myexactlog(8, 0)
        if a[i] == 0:
            myexactlog(9, 1)
            count_zero += 1
            myexactlog(10, count_zero)
            continue
        if a[i] < 0:
            myexactlog(11, 2)
            count_neg += 1
            myexactlog(12, count_neg)
            max_neg = max(max_neg, a[i])
            myexactlog(13, max_neg)
        prod = prod * a[i]
        myexactlog(14, prod)
        break
    if count_zero == n:
        myexactlog(15, 3)
        myexactlog(16, 0)
        return 0
    if count_neg & 1:
        myexactlog(17, 5)
        if count_neg == 1 and count_zero > 0 and count_zero + count_neg == n:
            myexactlog(18, 4)
            myexactlog(19, 0)
            return 0
        prod = int(prod / max_neg)
        myexactlog(20, prod)