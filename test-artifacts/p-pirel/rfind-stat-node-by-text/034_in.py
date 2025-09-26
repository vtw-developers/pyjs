def f_gold(arr1, arr2, m, n):
    i = 0
    j = 0
    if m < n:
        return 0
    arr1.sort()
    arr2.sort()
    while i < n and j < m:
        if arr1[j] < arr2[i]:
            j += 1
        elif arr1[j] == arr2[i]:
            j += 1
            i += 1
        else:
            return 0