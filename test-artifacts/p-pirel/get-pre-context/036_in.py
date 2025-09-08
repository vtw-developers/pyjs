def f_gold(arr, low, high, x):
    if x <= arr[low]:
        return low
    for i in range(low, high - 1):
        if arr[i] < x and arr[i + 1] >= x:
            return i + 1
    return -1