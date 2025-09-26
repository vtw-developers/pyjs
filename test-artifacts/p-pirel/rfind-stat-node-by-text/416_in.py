def f_gold(a, n):
    if n == 1:
        retval_1 = a[0]
        return retval_1
    max_neg = float("-inf")
    min_pos = float("inf")
    count_neg = 0
    count_zero = 0
    prod = 1
    for i in range(0, n):
        if a[i] == 0:
            count_zero = count_zero + 1
            continue
        if a[i] < 0:
            count_neg = count_neg + 1
            max_neg = max(max_neg, a[i])
        if a[i] > 0:
            min_pos = min(min_pos, a[i])
        prod = prod * a[i]
    if count_zero == n or (count_neg == 0 and count_zero > 0):
        return 0