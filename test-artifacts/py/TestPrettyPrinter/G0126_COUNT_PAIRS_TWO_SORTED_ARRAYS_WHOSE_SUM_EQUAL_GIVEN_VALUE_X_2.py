def f_gold(arr1, arr2, m, n, x):
    count, l, r = 0, 0, n - 1
    while l < m and r >= 0:
        if (arr1[l] + arr2[r]) == x:
            l += 1
            r -= 1
            count += 1
        elif (arr1[l] + arr2[r]) < x:
            l += 1
        else:
            r -= 1
    return count