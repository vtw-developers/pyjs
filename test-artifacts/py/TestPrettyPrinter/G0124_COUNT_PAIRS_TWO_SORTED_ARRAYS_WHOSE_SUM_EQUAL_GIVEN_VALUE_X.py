def f_gold(arr1, arr2, m, n, x):
    count = 0
    for i in range(m):
        for j in range(n):
            if arr1[i] + arr2[j] == x:
                count = count + 1
    return count