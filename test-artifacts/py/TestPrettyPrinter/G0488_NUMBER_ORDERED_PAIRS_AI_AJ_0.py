def f_gold(a, n):
    count = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            if (a[i] & a[j]) == 0:
                count += 2
    return count