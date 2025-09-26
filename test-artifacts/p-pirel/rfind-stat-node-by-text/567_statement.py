if count_neg & 1:
    if count_neg == 1 and count_zero > 0 and count_zero + count_neg == n:
        return 0
    prod = int(prod / max_neg)