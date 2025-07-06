def f_gold(arr, n):
    arr.sort()
    return arr[n - 1] + arr[n - 2] + arr[n - 3]