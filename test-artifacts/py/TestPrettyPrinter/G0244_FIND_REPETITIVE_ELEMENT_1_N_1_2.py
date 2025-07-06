def f_gold(arr, n):
    res = 0
    for i in range(0, n - 1):
        res = res ^ (i + 1) ^ arr[i]
    res = res ^ arr[n - 1]
    return res