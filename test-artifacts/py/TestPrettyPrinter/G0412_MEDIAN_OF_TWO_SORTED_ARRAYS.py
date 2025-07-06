def f_gold(ar1, ar2, n):
    i = 0
    j = 0
    m1 = -1
    m2 = -1
    count = 0
    while count < n + 1:
        count += 1
        if i == n:
            m1 = m2
            m2 = ar2[0]
            break
        elif j == n:
            m1 = m2
            m2 = ar1[0]
            break
        if ar1[i] < ar2[j]:
            m1 = m2
            m2 = ar1[i]
            i += 1
        else:
            m1 = m2
            m2 = ar2[j]
            j += 1
    return (m1 + m2) / 2