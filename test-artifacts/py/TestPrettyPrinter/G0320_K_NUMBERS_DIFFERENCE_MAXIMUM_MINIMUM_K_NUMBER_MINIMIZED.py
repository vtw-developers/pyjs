def f_gold(arr, n, k):
    result = +2147483647
    arr.sort()
    for i in range(n - k + 1):
        result = int(min(result, arr[i + k - 1] - arr[i]))
    return result