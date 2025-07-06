def f_gold(arr, n, x):
    res = 0
    for i in range(n):
        if x == arr[i]:
            res += 1
    return res