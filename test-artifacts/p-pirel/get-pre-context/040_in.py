def f_gold(arr, low, high, x):
    if x <= arr[low]:
        myexactlog(1, 0)
        myexactlog(2, low)
        return low
    if x > arr[high]:
        myexactlog(3, 1)
        myexactlog(4, -1)
        return -1
    mid = (low + high) // 2
    myexactlog(5, mid)
    if arr[mid] == x:
        myexactlog(6, 3)
        myexactlog(7, mid)
        return mid
    elif arr[mid] < x:
        myexactlog(8, 0)
        if mid + 1 <= high and x <= arr[mid + 1]:
            myexactlog(9, 2)
            pass
        else:
            myexactlog(10, 0)
            pass
    else:
        myexactlog(11, 1)
        pass