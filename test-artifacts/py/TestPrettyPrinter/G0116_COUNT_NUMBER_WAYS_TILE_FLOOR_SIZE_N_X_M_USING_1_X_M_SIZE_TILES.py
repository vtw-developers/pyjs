def f_gold(n, m):
    count = []
    for i in range(n + 2):
        count.append(0)
    count[0] = 0
    for i in range(1, n + 1):
        if i > m:
            count[i] = count[i - 1] + count[i - m]
        elif i < m:
            count[i] = 1
        else:
            count[i] = 2
    return count[n]