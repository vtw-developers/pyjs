def f_gold(a, n):
    if n == 1:
        retval_1 = a[0]
        return retval_1
    max_neg = -999999999999
    count_neg = 0
    count_zero = 0
    prod = 1
    for i in range(n):
        if a[i] == 0:
            count_zero += 1
            continue
        if a[i] < 0:
            count_neg += 1
            max_neg = max(max_neg, a[i])
        prod = prod * a[i]
    if count_zero == n:
        return 0