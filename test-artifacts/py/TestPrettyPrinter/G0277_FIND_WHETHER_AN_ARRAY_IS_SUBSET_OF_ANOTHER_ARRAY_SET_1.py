def f_gold(arr1, arr2, m, n):
    i = 0
    j = 0
    for i in range(n):
        for j in range(m):
            if arr2[i] == arr1[j]:
                break
        if j == m:
            return 0
    return 1