def f_gold(arr, n, x):
    i = 0
    while i <= n - 1:
        if arr[i] == x:
            return i
        i += abs(arr[i] - x)
    return -1