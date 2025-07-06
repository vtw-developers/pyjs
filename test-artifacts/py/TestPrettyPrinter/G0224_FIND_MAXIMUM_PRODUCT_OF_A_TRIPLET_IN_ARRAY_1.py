def f_gold(arr, n):
    if n < 3:
        return -1
    arr.sort()
    return max(arr[0] * arr[1] * arr[n - 1], arr[n - 1] * arr[n - 2] * arr[n - 3])