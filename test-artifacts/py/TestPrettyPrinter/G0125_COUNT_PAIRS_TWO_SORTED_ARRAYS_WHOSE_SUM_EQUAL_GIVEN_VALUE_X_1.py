def f_gold(arr1, arr2, m, n, x):
    count = 0
    us = set()
    for i in range(m):
        us.add(arr1[i])
    for j in range(n):
        if x - arr2[j] in us:
            count += 1
    return count