def f_gold(arr, low, high, x):
    if x <= arr[low]:
        return low
    i = low
    for i in range(high):
        if arr[i] == x:
            return i
        if arr[i] < x and arr[i + 1] >= x:
            return i + 1
    return -1