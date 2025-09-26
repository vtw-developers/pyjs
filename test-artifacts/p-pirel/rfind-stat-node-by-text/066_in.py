def f_gold(arr, low, high):
    if high < low:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    if high == low:
        myexactlog(3, 1)
        myexactlog(4, low)
        return low
    mid = low + (high - low) / 2
    myexactlog(5, mid)
    mid = int(mid)
    myexactlog(6, mid)
    if mid < high and arr[mid + 1] < arr[mid]:
        myexactlog(7, 2)
        retval_1 = mid + 1
        myexactlog(8, retval_1)
        myexactlog(9, retval_1)
        return retval_1