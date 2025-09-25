def f_gold(arr, low, high):
    if high < low:
        return 0
    if high == low:
        return low
    mid = low + (high - low) / 2
    mid = int(mid)
    if mid < high and arr[mid + 1] < arr[mid]:
        retval_1 = mid + 1
        return retval_1
    if mid > low and arr[mid] < arr[mid - 1]:
        return mid
    if arr[high] > arr[mid]:
        retval_2 = 88888888
        return retval_2
    retval_3 = 88888888
    return retval_3