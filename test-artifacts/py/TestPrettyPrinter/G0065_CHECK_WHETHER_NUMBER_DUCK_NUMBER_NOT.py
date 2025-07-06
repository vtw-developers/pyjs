def f_gold(num):
    l = len(num)
    count_zero = 0
    i = 1
    while i < l:
        ch = num[i]
        if ch == "0":
            count_zero = count_zero + 1
        i = i + 1
    return count_zero