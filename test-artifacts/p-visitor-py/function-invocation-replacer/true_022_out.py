def f_gold(arr, low, high, x):
    if low > high:
        return -1
    if x >= arr[high]:
        return high
    mid = int((low + high) / 2)
    if arr[mid] == x:
        return mid
    if mid > 0 and arr[mid - 1] <= x and x < arr[mid]:
        return mid - 1
    if x < arr[mid]:
        return True
    return True